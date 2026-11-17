#!/usr/bin/env python3
"""Prédire une intention MASSIVE avec l'adaptateur QLoRA sur un GPU NVIDIA.

Utilisation après extraction de l'archive :
    python predict_gemma4_massive.py "Allume la lumière du salon" \
        --results-dir /content/gemma4_massive_fr_1000

Le dossier doit contenir adapter/, run_config.json et system_prompt.txt.
Utiliser le même environnement Python que pour l'entraînement.
"""

import argparse
import contextlib
import json
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phrase", help="Demande en français à classifier.")
    parser.add_argument(
        "--results-dir", type=Path, required=True,
        help="Racine des résultats extraits, contenant le dossier adapter/.",
    )
    args = parser.parse_args()
    if not args.phrase.strip():
        parser.error("La phrase ne doit pas être vide.")

    results_dir = args.results_dir.expanduser().resolve()
    adapter_dir = results_dir / "adapter"
    config_path = results_dir / "run_config.json"
    prompt_path = results_dir / "system_prompt.txt"
    for path in (config_path, prompt_path, adapter_dir / "adapter_config.json"):
        if not path.is_file():
            parser.error(f"Fichier introuvable : {path}")

    config = json.loads(config_path.read_text(encoding="utf-8"))
    model_id = config.get("model_id")
    revision = config.get("model_revision")
    if not model_id or not revision:
        parser.error("run_config.json doit préciser model_id et model_revision.")
    system_prompt = prompt_path.read_text(encoding="utf-8")

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    if not torch.cuda.is_available():
        parser.error("Un GPU NVIDIA avec CUDA est requis pour cette inférence 4 bits.")

    # Réserver stdout à l'étiquette ; les informations de chargement vont sur stderr.
    with contextlib.redirect_stdout(sys.stderr):
        tokenizer = AutoTokenizer.from_pretrained(
            str(adapter_dir), local_files_only=True,
        )
        base_model = AutoModelForCausalLM.from_pretrained(
            model_id,
            revision=revision,
            dtype=torch.float16,
            device_map={"": 0},
            attn_implementation="sdpa",
            quantization_config=BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.float16,
            ),
        )
        model = PeftModel.from_pretrained(base_model, str(adapter_dir))
        model.eval()
        model.config.use_cache = True

        prompt = tokenizer.apply_chat_template(
            [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": args.phrase},
            ],
            tokenize=False,
            add_generation_prompt=True,
            enable_thinking=False,
        )
        inputs = tokenizer(
            prompt, add_special_tokens=False, return_tensors="pt",
        ).to("cuda:0")
        end_id = tokenizer.get_vocab().get("<turn|>")
        if end_id is None:
            parser.error("Le tokenizer sauvegardé ne contient pas le token Gemma 4 <turn|>.")

        max_new_tokens = 20
        audit_path = results_dir / "data" / "data_audit.json"
        if audit_path.is_file():
            intent_names = json.loads(audit_path.read_text(encoding="utf-8")).get("intent_names")
            if intent_names:
                max_new_tokens = max(
                    len(tokenizer(label, add_special_tokens=False)["input_ids"])
                    for label in intent_names
                ) + 4

        with torch.inference_mode(), torch.autocast("cuda", dtype=torch.float16):
            output = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                eos_token_id=end_id,
                pad_token_id=tokenizer.pad_token_id,
                use_cache=True,
            )
        label = tokenizer.decode(
            output[0, inputs["input_ids"].shape[1]:], skip_special_tokens=True,
        ).strip()

    print(label)


if __name__ == "__main__":
    main()

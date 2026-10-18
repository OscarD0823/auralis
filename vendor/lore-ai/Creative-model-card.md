---
base_model: huihui-ai/Qwen2.5-0.5B-Instruct-abliterated-v3
language:
- zho
- eng
- fra
- spa
- por
- deu
- ita
- rus
- jpn
- kor
- vie
- tha
- ara
library_name: transformers
license: apache-2.0
license_link: https://huggingface.co/huihui-ai/Qwen2.5-0.5B-Instruct-abliterated-v3/blob/main/LICENSE
mradermacher:
  readme_rev: 1
quantized_by: mradermacher
tags:
- chat
- abliterated
- uncensored
---
## About

<!-- ### quantize_version: 2 -->
<!-- ### output_tensor_quantised: 1 -->
<!-- ### convert_type: hf -->
<!-- ### vocab_type:  -->
<!-- ### tags:  -->
static quants of https://huggingface.co/huihui-ai/Qwen2.5-0.5B-Instruct-abliterated-v3

<!-- provided-files -->

***For a convenient overview and download list, visit our [model page for this model](https://hf.tst.eu/model#Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF).***

weighted/imatrix quants are available at https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-i1-GGUF
## Usage

If you are unsure how to use GGUF files, refer to one of [TheBloke's
READMEs](https://huggingface.co/TheBloke/KafkaLM-70B-German-V0.1-GGUF) for
more details, including on how to concatenate multi-part files.

## Provided Quants

(sorted by size, not necessarily quality. IQ-quants are often preferable over similar sized non-IQ quants)

| Link | Type | Size/GB | Notes |
|:-----|:-----|--------:|:------|
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q3_K_S.gguf) | Q3_K_S | 0.4 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q2_K.gguf) | Q2_K | 0.4 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.IQ4_XS.gguf) | IQ4_XS | 0.5 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q3_K_M.gguf) | Q3_K_M | 0.5 | lower quality |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q3_K_L.gguf) | Q3_K_L | 0.5 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q4_K_S.gguf) | Q4_K_S | 0.5 | fast, recommended |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q4_K_M.gguf) | Q4_K_M | 0.5 | fast, recommended |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q5_K_S.gguf) | Q5_K_S | 0.5 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q5_K_M.gguf) | Q5_K_M | 0.5 |  |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q6_K.gguf) | Q6_K | 0.6 | very good quality |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.Q8_0.gguf) | Q8_0 | 0.6 | fast, best quality |
| [GGUF](https://huggingface.co/mradermacher/Qwen2.5-0.5B-Instruct-abliterated-v3-GGUF/resolve/main/Qwen2.5-0.5B-Instruct-abliterated-v3.f16.gguf) | f16 | 1.1 | 16 bpw, overkill |

Here is a handy graph by ikawrakow comparing some lower-quality quant
types (lower is better):

![image.png](https://www.nethype.de/huggingface_embed/quantpplgraph.png)

And here are Artefact2's thoughts on the matter:
https://gist.github.com/Artefact2/b5f810600771265fc1e39442288e8ec9

## FAQ / Model Request

See https://huggingface.co/mradermacher/model_requests for some answers to
questions you might have and/or if you want some other model quantized.

## Thanks

I thank my company, [nethype GmbH](https://www.nethype.de/), for letting
me use its servers and providing upgrades to my workstation to enable
this work in my free time.

<!-- end -->

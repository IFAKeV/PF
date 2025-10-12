# Generating the Car Illustrations

This project does not include an image generation backend. To turn the prompt templates in this folder into actual pictures, you will need to use an external text-to-image service or run a local diffusion model. The sections below outline common approaches.

## Cloud or Hosted Generators
- **OpenAI DALL·E / Images API** – Paste one of the prompts into the Images Playground or call the `images.generate` endpoint. Set the aspect ratio to landscape (e.g., `"1024x768"`).
- **Midjourney / Adobe Firefly / Leonardo** – These services support custom prompts and aspect-ratio flags (for example Midjourney’s `--ar 16:9`).
- **Stability AI DreamStudio** – Select the Stable Diffusion model, choose a landscape size, and use the prompts as provided.

These platforms usually provide sliders or advanced settings (guidance scale, stylization). Start with the defaults, then adjust if you need more line-art contrast or crisper outlines.

## Local, Open-Source Options
If you prefer to generate images on your own hardware, you can install a Stable Diffusion interface such as:

1. **AUTOMATIC1111 Web UI** – https://github.com/AUTOMATIC1111/stable-diffusion-webui
   - Install the Web UI following the README.
   - Download a diffusion checkpoint that supports clean line art (e.g., `DreamShaper`, `Juggernaut`, or an "ink" tuned model).
   - Paste the prompt into the text field, set width larger than height (for example `960x640`), and enable high-res fix if the model supports it.
2. **InvokeAI** – https://github.com/invoke-ai/InvokeAI (includes a guided install script and an easy aspect ratio selector).
3. **ComfyUI** – A node-based interface that can be customized for vector-like results.

### Tips for Local Runs
- Add a negative prompt with terms like `blurry, noisy, low detail` to keep the line art crisp.
- If the model creates a background, increase the weight of `WHITE background` or add `plain studio background` to the prompt.
- For consistent side views, lower the random seed variation or reuse a seed that produced a good render.

## About Ollama
Ollama is currently focused on serving language models locally. It does **not** provide an official text-to-image model, so you cannot generate pictures directly through `ollama run` alone. Some community projects experiment with wrapping Stable Diffusion or Flux around an Ollama-like interface, but they require separate model downloads and setup scripts that are outside the scope of this repository.

If you would like a local experience similar to Ollama for diffusion models, consider using the tools above or running a Docker image of Automatic1111/InvokeAI. You can still use Ollama alongside them—for example, to iterate on prompt wording with an LLM—and then paste the refined text into your diffusion UI.

## Keeping Prompts Organized
- Save successful renders with filenames that reference the prompt file (e.g., `volvo_c30_seed1234.png`).
- Store metadata (model name, sampler, guidance scale, seed) so you can reproduce a favorite look later.

With these options you can turn the provided prompt templates into the requested landscape illustrations of each car.

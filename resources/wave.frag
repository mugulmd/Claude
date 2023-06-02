#version 330

uniform vec2 resolution;
uniform float time;

uniform float freq = 1.0;
uniform float amp = 0.1;
uniform vec3 water = vec3(0.0, 0.0, 1.0);
uniform vec3 sky = vec3(1.0);
uniform int nb_waves = 1;

out vec3 frag_color;

void main() {
    // Retrieve, normalize and unsqueeze fragment coordinates
    vec2 uv = gl_FragCoord.xy / resolution;
    uv = 2.0 * uv - 1.0;
    uv.x *= resolution.x / resolution.y;

    // Compute Y threshold based on X for wave shape
    float freq_clamped = clamp(freq, 0.1, 100.0);
    float amp_clamped = clamp(amp, 0.01, 1.0);
    float wave = sin((time + uv.x) * freq) * amp_clamped;

    // Compute wave level based on number of waves
    float nb_waves_clamped = float(max(nb_waves, 1));
    float level = floor((uv.y - wave + 1.0) * 0.5 * (nb_waves_clamped + 1.0));
    float level_clamped = clamp(level, 0, nb_waves_clamped);

    // Compute output color based on level by interpolation
    frag_color = mix(water, sky, level_clamped / nb_waves_clamped);
}

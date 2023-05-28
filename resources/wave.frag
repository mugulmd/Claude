#version 330

uniform vec2 resolution;
uniform float time;

uniform float freq;
uniform float amp;

out vec3 frag_color;

void main() {
    // Retrieve, normalize and unsqueeze fragment coordinates
    vec2 uv = gl_FragCoord.xy / resolution;
    uv = 2.0 * uv - 1.0;
    uv.x *= resolution.x / resolution.y;

    // Compute Y threshold based on X for wave shape
    float freq_clamped = clamp(freq, 0.1, 100.0);
    float amp_clamped = clamp(amp, 0.01, 1.0);
    float threshold = sin((time + uv.x) * freq) * amp_clamped;

    // Write output color
    if (uv.y < threshold) {
        frag_color = vec3(0.0);
    } else {
        frag_color = vec3(1.0);
    }
}

// A collection of useful shader code pieces


// Retrieve, normalize and unsqueeze fragment coordinates
vec2 uv = gl_FragCoord.xy / resolution;
uv = 2.0 * uv - 1.0;
uv.x *= resolution.x / resolution.y;

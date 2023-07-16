// A collection of useful shader code pieces


// Retrieve, normalize and unsqueeze fragment coordinates
vec2 uv = gl_FragCoord.xy / resolution;
uv = 2.0 * uv - 1.0;
uv.x *= resolution.x / resolution.y;


mat2 rot(float a) {
    float c = cos(a);
    float s = sin(a);
    return mat2(c, -s, s, c);
}


float rand(vec2 s) {
    return fract(sin(dot(s, vec2(1321.1241, 125.2134)) * 74.57));
}


ivec2 pixelate(vec2 uv, float size) {
    return ivec2(floor(uv / size));
}


float gyroid(vec3 p) {
    return dot(sin(p), cos(p.yzx));
}

#version 330

in vec3 normal;
in vec3 frag_pos;
in float height;

out vec4 frag_color;

uniform vec3 light_pos;
uniform vec3 view_pos;
uniform vec3 light_color;

vec3 getColor(float h) {
    if (h < 1.5) return vec3(0.0, 0.3, 0.8);      // agua
    else if (h < 3.5) return vec3(0.95, 0.85, 0.6); // arena
    else if (h < 6.0) return vec3(0.1, 0.6, 0.1);   // pasto
    else if (h < 9.0) return vec3(0.5, 0.4, 0.3);   // montaña
    else return vec3(1.0, 1.0, 1.0);                // nieve
}

void main() {
    vec3 object_color = getColor(height);

    // Luz ambiental
    float ambient_strength = 0.2;
    vec3 ambient = ambient_strength * light_color;

    // Difusa
    vec3 norm = normalize(normal);
    vec3 light_dir = normalize(light_pos - frag_pos);
    float diff = max(dot(norm, light_dir), 0.0);
    vec3 diffuse = diff * light_color;

    // Especular
    float specular_strength = 0.3;
    vec3 view_dir = normalize(view_pos - frag_pos);
    vec3 reflect_dir = reflect(-light_dir, norm);
    float spec = pow(max(dot(view_dir, reflect_dir), 0.0), 32);
    vec3 specular = specular_strength * spec * light_color;

    vec3 result = (ambient + diffuse + specular) * object_color;
    frag_color = vec4(result, 1.0);
}

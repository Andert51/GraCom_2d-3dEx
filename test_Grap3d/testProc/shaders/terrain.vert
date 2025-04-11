#version 330

in vec3 in_position;
in vec3 in_normal;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

out vec3 normal;
out vec3 frag_pos;
out float height;

void main() {
    vec4 world_pos = model * vec4(in_position, 1.0);
    frag_pos = vec3(world_pos);
    normal = mat3(transpose(inverse(model))) * in_normal;
    height = in_position.y;
    gl_Position = projection * view * world_pos;
}

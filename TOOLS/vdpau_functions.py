#!/usr/bin/env python

# Generate vdpau_template.c

functions = """
# get_error_string should be first, because the function lookup loop should
# have it available to print errors for other functions
get_error_string

bitmap_surface_create
bitmap_surface_destroy
bitmap_surface_put_bits_native
bitmap_surface_query_capabilities
decoder_create
decoder_destroy
decoder_render
device_destroy
generate_csc_matrix GenerateCSCMatrix  # CSC completely capitalized
output_surface_create
output_surface_destroy
output_surface_get_bits_native
output_surface_put_bits_indexed
output_surface_put_bits_native
output_surface_render_bitmap_surface
output_surface_render_output_surface
preemption_callback_register
presentation_queue_block_until_surface_idle
presentation_queue_create
presentation_queue_destroy
presentation_queue_display
presentation_queue_get_time
presentation_queue_query_surface_status
presentation_queue_target_create_x11
presentation_queue_target_destroy
video_mixer_create
video_mixer_destroy
video_mixer_query_feature_support
video_mixer_render
video_mixer_set_attribute_values
video_mixer_set_feature_enables
video_surface_create
video_surface_destroy
video_surface_put_bits_y_cb_cr
"""

print("""
/* List the VDPAU functions used by MPlayer.
 * Generated by vdpau_functions.py.
 * First argument on each line is the VDPAU function type name,
 * second macro name needed to get function address,
 * third name MPlayer uses for the function.
 */
""")
for line in functions.splitlines():
    parts = line.split('#')[0].strip().split()
    if not parts:
        continue  # empty/comment line
    if len(parts) > 1:
        mp_name, vdpau_name = parts
    else:
        mp_name = parts[0]
        vdpau_name = ''.join(part.capitalize() for part in mp_name.split('_'))
    macro_name = mp_name.upper()
    print('VDP_FUNCTION(Vdp%s, VDP_FUNC_ID_%s, %s)' % (vdpau_name, macro_name, mp_name))

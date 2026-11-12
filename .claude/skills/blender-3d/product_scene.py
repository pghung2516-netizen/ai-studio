"""Bộ hàm dựng cảnh sản phẩm 3D cho Blender (Claude gửi qua execute_blender_code).

Cách dùng: đọc file này, dán nội dung + vài dòng gọi hàm ở cuối vào `code`.
Chỉ dùng bpy / bmesh / mathutils / math (qua được chế độ an toàn BLENDER_MCP_SAFE_MODE=1).
Đường dẫn file: Claude tính sẵn rồi dán vào dạng chuỗi (không dùng os/open ở đây).
Blender 3.0+; chạy tốt trên 4.x. CHƯA thử trên Blender thật - nếu lỗi, sửa nhỏ rồi chạy lại.
"""
import math
import bpy


def clear_scene():
    """Xóa sạch cảnh mặc định (khối lập phương, đèn, camera)."""
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()
    for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
        for block in list(coll):
            if block.users == 0:
                coll.remove(block)


def set_engine_eevee(samples=32):
    """Eevee = nhanh. Tên engine khác nhau giữa các bản Blender nên thử lần lượt."""
    scene = bpy.context.scene
    names = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    for name in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
        if name in names:
            scene.render.engine = name
            break
    try:
        scene.eevee.taa_render_samples = samples
    except Exception:
        pass
    scene.view_settings.view_transform = "Standard"  # giữ đúng màu sản phẩm


def simple_material(name, rgba, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = rgba
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    return mat


def image_material(name, image_path, roughness=0.45, alpha=False):
    """Vật liệu dán ảnh (ảnh sản phẩm / hoa văn bao bì). alpha=True nếu ảnh PNG đã xóa nền."""
    img = bpy.data.images.load(image_path)
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nt = mat.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = roughness
    if alpha:
        nt.links.new(tex.outputs["Alpha"], bsdf.inputs["Alpha"])
        try:
            mat.blend_method = "BLEND"
        except Exception:
            pass
    return mat, img


def studio_floor(color=(0.92, 0.92, 0.92, 1.0), size=20.0):
    """Sàn + nền trắng/xám nhẹ kiểu studio chụp sản phẩm."""
    bpy.ops.mesh.primitive_plane_add(size=size, location=(0, 0, 0))
    floor = bpy.context.active_object
    floor.name = "San"
    floor.data.materials.append(simple_material("San", color, roughness=0.6))
    world = bpy.context.scene.world or bpy.data.worlds.new("World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = color
    bg.inputs["Strength"].default_value = 0.6
    return floor


def product_box(width=1.0, depth=0.6, height=1.4, image_path=None, color=(0.9, 0.2, 0.3, 1.0)):
    """Hộp đóng gói (hộp quà/hộp sản phẩm). Có image_path thì dán ảnh lên các mặt."""
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, height / 2))
    box = bpy.context.active_object
    box.name = "SanPham"
    box.scale = (width, depth, height)
    bpy.ops.object.transform_apply(scale=True)
    if image_path:
        mat, _ = image_material("BaoBi", image_path)
    else:
        mat = simple_material("BaoBi", color, roughness=0.35)
    box.data.materials.append(mat)
    return box


def product_card(image_path, height=1.4, alpha=True):
    """Ảnh sản phẩm (đã xóa nền) dựng đứng như tấm bảng. Hợp khi chỉ có 1 tấm ảnh."""
    mat, img = image_material("AnhSanPham", image_path, alpha=alpha)
    ratio = img.size[0] / max(img.size[1], 1)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, height / 2))
    card = bpy.context.active_object
    card.name = "SanPham"
    card.scale = (height * ratio, height, 1)
    card.rotation_euler = (math.radians(90), 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    card.data.materials.append(mat)
    return card


def three_point_lights(target_height=0.7, power=900):
    """Đèn 3 điểm: chính, bổ sung, ngược sáng. Đơn vị Watt (area light)."""
    specs = [("DenChinh", (3, -3, 3.5), power), ("DenPhu", (-3.5, -2, 2), power * 0.4),
             ("DenNguoc", (0, 4, 3), power * 0.7)]
    for name, loc, watt in specs:
        data = bpy.data.lights.new(name, "AREA")
        data.energy = watt
        data.size = 3.0
        obj = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(obj)
        obj.location = loc
        direction = bpy.context.scene.cursor.location.copy()
        direction.z = target_height
        look = direction - obj.location
        obj.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()


def add_camera(distance=4.0, height=1.2, target_height=0.7, lens=50):
    cam_data = bpy.data.cameras.new("Camera")
    cam_data.lens = lens
    cam = bpy.data.objects.new("Camera", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.location = (0, -distance, height)
    from mathutils import Vector
    look = Vector((0, 0, target_height)) - cam.location
    cam.rotation_euler = look.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    return cam


def set_output(width, height, filepath):
    """Cỡ ảnh + nơi lưu. Ví dụ dọc TikTok 1080x1920, vuông 1080x1080, ngang 1920x1080."""
    r = bpy.context.scene.render
    r.resolution_x, r.resolution_y, r.resolution_percentage = width, height, 100
    r.filepath = filepath


def render_still(filepath):
    """Render 1 ảnh PNG. Chặn Blender vài chục giây - bình thường."""
    r = bpy.context.scene.render
    r.image_settings.file_format = "PNG"
    r.filepath = filepath
    bpy.ops.render.render(write_still=True)
    return filepath


def setup_turntable(product, seconds=6, fps=30, mp4_path=None):
    """Cho sản phẩm xoay đúng 360 độ, lặp mượt. KHÔNG render ở đây (xem SKILL.md: render bằng dòng lệnh)."""
    scene = bpy.context.scene
    frames = int(seconds * fps)
    scene.render.fps = fps
    scene.frame_start, scene.frame_end = 1, frames
    product.rotation_mode = "XYZ"
    product.rotation_euler[2] = 0
    product.keyframe_insert("rotation_euler", index=2, frame=1)
    product.rotation_euler[2] = math.radians(360)
    product.keyframe_insert("rotation_euler", index=2, frame=frames + 1)  # +1: khung cuối không trùng khung đầu
    action = product.animation_data.action
    fcurves = getattr(action, "fcurves", None)
    if fcurves is None:  # Blender 5.x đổi cấu trúc: bỏ qua, vẫn xoay nhưng có thể không đều tốc độ
        fcurves = []
    for fc in fcurves:
        for kp in fc.keyframe_points:
            kp.interpolation = "LINEAR"
    if mp4_path:
        r = scene.render
        r.image_settings.file_format = "FFMPEG"
        r.ffmpeg.format = "MPEG4"
        r.ffmpeg.codec = "H264"
        r.ffmpeg.constant_rate_factor = "HIGH"
        r.filepath = mp4_path
    return frames


# --- Ví dụ gọi (Claude chỉnh đường dẫn rồi dán nối phía dưới) ---
# clear_scene(); set_engine_eevee(32); studio_floor()
# hop = product_box(image_path=r"C:\...\bao-bi.png")      # hoặc product_card(r"C:\...\sp-xoa-nen.png")
# three_point_lights(); add_camera()
# set_output(1080, 1920, r"C:\...\02-THANH-PHAM\2026-11-13\hop-qua-3d.png")
# render_still(r"C:\...\02-THANH-PHAM\2026-11-13\hop-qua-3d.png")
# --- Xoay 360: setup_turntable(hop, 6, 30, r"C:\...\hop-xoay.mp4"); rồi lưu .blend bằng
#     bpy.ops.wm.save_as_mainfile(filepath=r"C:\...\hop-xoay.blend") và render bằng dòng lệnh.

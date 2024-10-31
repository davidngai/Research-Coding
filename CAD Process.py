import xml.etree.ElementTree as ET
import os
import re  # 确保导入re模块

def change_layers_to_white(svg_file, output_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    # 递归遍历所有图层
    def change_color_to_white(layer):
        # 将图层变为白色
        for elem in layer.iter():
            if 'style' in elem.attrib:
                style = elem.attrib['style']
                style = re.sub(r'fill:\s*#[0-9a-fA-F]{6}', 'fill:#ffffff', style)
                style = re.sub(r'stroke:\s*#[0-9a-fA-F]{6}', 'stroke:#ffffff', style)
                elem.attrib['style'] = style

            if 'fill' in elem.attrib:
                elem.attrib['fill'] = '#ffffff'
            if 'stroke' in elem.attrib:
                elem.attrib['stroke'] = '#ffffff'

    # 递归查找并修改 Door 和 Window 图层
    def find_and_modify_layers(parent):
        for layer in parent.findall('.//{*}g'):
            layer_id = layer.get('id')
            layer_label = layer.get('label')  # 更通用的获取方法
            if layer_label and ('door' in layer_label.lower() or 'window' in layer_label.lower()):
                change_color_to_white(layer)
            elif layer_id and ('door' in layer_id.lower() or 'window' in layer_id.lower()):
                change_color_to_white(layer)
            else:
                find_and_modify_layers(layer)  # 递归检查子图层

    # 处理与 Wall 同级的其他图层
    def change_sibling_layers_to_white():
        for parent in root.findall('.//{*}g'):
            for layer in list(parent):
                layer_id = layer.get('id')
                layer_label = layer.get('label')  # 更通用的获取方法
                if layer_label and 'wall' in layer_label.lower() or layer_id and 'wall' in layer_id.lower():
                    for sibling in list(parent):
                        sibling_id = sibling.get('id')
                        sibling_label = sibling.get('label')
                        if sibling is not layer and not ('wall' in (sibling_label or '').lower() or 'wall' in (sibling_id or '').lower()):
                            change_color_to_white(sibling)

    # 从根节点开始查找 Door 和 Window 图层并修改颜色
    find_and_modify_layers(root)

    # 处理与 Wall 同级的其他图层
    change_sibling_layers_to_white()

    # 保存修改后的SVG文件到新的位置
    tree.write(output_file, xml_declaration=True, encoding='utf-8')

def batch_process_svg_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith('.svg'):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename)
            change_layers_to_white(input_file_path, output_file_path)
            print(f"已处理文件: {filename}")

# 输入和输出目录
input_directory = r"E:\CAD+GAN\01"
output_directory = r"E:\CAD+GAN\02"

# 批量处理SVG文件并将结果保存到新的目录
batch_process_svg_files(input_directory, output_directory)

print("所有符合条件的图层已变为白色，文件已保存到新目录。")

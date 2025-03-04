#!/bin/bash

# 指定目标目录
directory="MME_Benchmark"

# 检查目录是否存在
if [ -d "$directory" ]; then
    # 获取子文件夹总数用于进度条
    folder_count=$(find "$directory" -maxdepth 1 -mindepth 1 -type d | wc -l)
    current_folder=0
    
    # 获取MME_Benchmark的父目录并创建MME_Image文件夹
    parent_dir=$(dirname "$directory")
    mkdir -p "$parent_dir/MME_Image"
    
    # 复制失败的文件统计
    failed_files=0
    
    # 在MME_Image下创建所有MME_Benchmark的子文件夹并复制图片
    find "$directory" -maxdepth 1 -mindepth 1 -type d | while read subfolder; do
        folder=$(basename "$subfolder")
        
        # 更新进度条
        ((current_folder++))
        printf "\r处理进度: [%-50s] %d%% (%d/%d)" \
            "$(printf '#%.0s' $(seq 1 $((50 * current_folder / folder_count))))" \
            $((100 * current_folder / folder_count)) \
            "$current_folder" "$folder_count"
        
        # 创建对应的子文件夹
        mkdir -p "$parent_dir/MME_Image/$folder"
        
        # 检查根目录下的图片并复制
        for file in "$directory/$folder"/*.{jpg,jpeg,png,gif,bmp}; do
            if [ -f "$file" ]; then
                filename=$(basename "$file")
                cp "$file" "$parent_dir/MME_Image/$folder/"
                
                # 验证文件是否成功复制
                if ! [ -f "$parent_dir/MME_Image/$folder/$filename" ]; then
                    echo -e "\n复制失败: $file"
                    ((failed_files++))
                elif ! cmp -s "$file" "$parent_dir/MME_Image/$folder/$filename"; then
                    echo -e "\n复制校验失败: $file (文件内容不匹配)"
                    ((failed_files++))
                fi
            fi
        done
        
        # 检查images目录下的图片并复制（如果存在）
        if [ -d "$directory/$folder/images" ]; then
            for file in "$directory/$folder/images"/*.{jpg,jpeg,png,gif,bmp}; do
                if [ -f "$file" ]; then
                    filename=$(basename "$file")
                    cp "$file" "$parent_dir/MME_Image/$folder/"
                    
                    # 验证文件是否成功复制
                    if ! [ -f "$parent_dir/MME_Image/$folder/$filename" ]; then
                        echo -e "\n复制失败: $file"
                        ((failed_files++))
                    elif ! cmp -s "$file" "$parent_dir/MME_Image/$folder/$filename"; then
                        echo -e "\n复制校验失败: $file (文件内容不匹配)"
                        ((failed_files++))
                    fi
                fi
            done
        fi
    done
    
    # 确保进度条显示100%
    printf "\r处理进度: [%-50s] 100%% (%d/%d)\n" \
        "$(printf '#%.0s' $(seq 1 50))" "$folder_count" "$folder_count"
    
    # 复制完成后的总结
    if [ $failed_files -eq 0 ]; then
        echo "所有图片复制成功!"
    else
        echo "警告: $failed_files 个文件复制失败或内容不匹配"
        exit 1
    fi
else
    echo "错误：目录 $directory 不存在"
    exit 1
fi
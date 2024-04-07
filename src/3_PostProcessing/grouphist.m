clearvars;
clc;

% 載入資料
path = 'C:\Users\dulci\OneDrive - 國立陽明交通大學\桌面\NYCU\0006_大專生計畫\SHM-MIE\result\TCUBA6_交大公教宿舍_濾波_30_3_3\MIE_Minus_floor1th_scale0th';
save_path_2D = 'C:\Users\dulci\OneDrive - 國立陽明交通大學\桌面\NYCU\0006_大專生計畫\SHM-MIE\result\TCUBA6_交大公教宿舍_濾波_30_3_3\DMIE_2D';
save_path_3D = 'C:\Users\dulci\OneDrive - 國立陽明交通大學\桌面\NYCU\0006_大專生計畫\SHM-MIE\result\TCUBA6_交大公教宿舍_濾波_30_3_3\DMIE_3D';


files = dir(fullfile(path, '*.txt'));
[status, message, messageid] = mkdir(save_path_2D);
[status, message, messageid] = mkdir(save_path_3D);

%{
% 繪製 scatter plot
figure('Position', [0, 0, 500, 500]);

% 繪製 2D 熱力圖
for fileIdx = 1:numel(files)
    data = load(fullfile(path, files(fileIdx).name));
    data_matrix = reshape(data, 5, 30);
    
    % 清除當前圖形
    clf;
    
    % 使用 imagesc 函數繪製 2D 熱力圖
    imagesc(data_matrix');
    
    % 將數值範圍限制在一個特定的範圍，例如 -2 到 2
    caxis([0 4.5]);
    
    % 將顏色軸刻度設置為相同的顏色
    colormap("turbo");
    
    % 移除座標軸和顏色軸
    axis off;
    colorbar off;
    
    % 儲存圖像
    [~, filename, ~] = fileparts(files(fileIdx).name);
    save_fullpath = fullfile(save_path_2D, [filename, '.png']);
    saveas(gcf, save_fullpath);
end

%}
files = dir(fullfile(path, '*.txt'));
[status, message, messageid] = mkdir(save_path_2D);
[status, message, messageid] = mkdir(save_path_3D);

for fileIdx = 1:numel(files)
    data = load(fullfile(path, files(fileIdx).name));
    data_matrix = reshape(data, 5, 30);
    
    % 使用 surf 函數繪製 3D 圖，將 x 軸和 y 軸交換
    surf(data_matrix', 'EdgeColor', 'none');
    view(15, 40); % 第一個參數是方位角，第二個參數是仰角
    % 設置 x 軸和 y 軸的刻度
    set(gca, 'XTick', [1:7]);
    set(gca, 'XTickLabel', {'B2~1F', '1F~3F', '3F~7F', '7F~14F'});
    % 將數值範圍限制在一個特定的範圍，例如 -2 到 2
    clim([-2.5, 1.5]);
    
    % 將顏色軸刻度設置為相同的顏色
    colormap("turbo");%gray
    
    grid on;
    colorbar;
    
    % 添加標題和軸標籤，注意交換了 x 和 y 的標籤
    title(files(fileIdx).name);
    xlabel('floor');
    ylabel('Scale');
    zlabel('DMIE');
    zlim([-2.5, 1.5]); %
    [~, filename, ~] = fileparts(files(fileIdx).name);
    save_fullpath = fullfile(save_path_3D, [filename, '.png']);
    saveas(gcf, save_fullpath);
    
    close(gcf);
    % 清除當前圖形
    clf;
end


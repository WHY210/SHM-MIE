clearvars;
clc;

% 載入資料
path = 'D:\SHM-MIE\result\min微振段_七層鋼構架樓層破壞_特定樓層_30_3_3\MIE';
save_path_2D = 'D:\SHM-MIE\result\min微振段_七層鋼構架樓層破壞_特定樓層_30_3_3\MIE_2D';
save_path_3D = 'D:\SHM-MIE\result\min微振段_七層鋼構架樓層破壞_特定樓層_30_3_3\MIE_3D';


files = dir(fullfile(path, '*.txt'));
[status, message, messageid] = mkdir(save_path_2D);
[status, message, messageid] = mkdir(save_path_3D);


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

%{
files = dir(fullfile(path, '*.txt'));
[status, message, messageid] = mkdir(save_path_2D);
[status, message, messageid] = mkdir(save_path_3D);

for fileIdx = 1:numel(files)
    data = load(fullfile(path, files(fileIdx).name));
    data_matrix = reshape(data, 4, 30);
    
    % 使用 surf 函數繪製 3D 圖，將 x 軸和 y 軸交換
    surf(data_matrix', 'EdgeColor', 'none');
    view(15, 40); % 第一個參數是方位角，第二個參數是仰角
    % 設置 x 軸和 y 軸的刻度
    set(gca, 'XTick', [1:7]);
    set(gca, 'XTickLabel', {'0F~1F', '1F~3F', '3F~5F', '5F~7F'});
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
%}

clearvars;
clc;

% 輸入和輸出資料夾的路徑
input_path_TCUBA6 = "D:\0005_大專生計畫\04_MIE\data\TCUBA6_交大公教宿舍";
output_path_TCUBA6 = "D:\0005_大專生計畫\04_MIE\data\TCUBA6_交大公教宿舍";
% 取得資料夾中的所有檔案
file_list = dir(fullfile(input_path_TCUBA6, '*.txt'));

% 迴圈遍歷每個檔案
for i = 1:numel(file_list)
    filename = file_list(i).name;
    filterTCUBA6(input_path_TCUBA6, filename, output_path_TCUBA6)
end

%% FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function filterTCUBA6(input_path_TCUBA6, input_file_name, output_path_TCUBA6)
    
    output_file_name = input_file_name;
    
    % 讀取輸入（TCUBA6那種）
    input_file = fopen(fullfile(input_path_TCUBA6, input_file_name));
    a2 = cell(1, 24);
    a2{1} = textscan(input_file, ' %f ', 'HeaderLines', 10);
    min_length = length(a2{1}{1}); % 最短信號的長度
    for i = 2:24
        a2{i} = textscan(input_file, ' %f ', 'HeaderLines', 1);
        min_length = min(min_length, length(a2{i}{1})); % 更新最短信號的長度
    end
    fclose(input_file);

    
    % 創建一個新的圖形
    figure('Units', 'inches', 'Position', [0, 0, 20, 10]);
    
    % 迴圈畫出每一個channel的子圖
    for i = 1:24
        subplot(6, 4, i);
        plot(a2{i}{1}, 'r');
        ylim([-25, 25]); % 設置y值範圍
        grid on;
        title(['Channel ', num2str(i)], 'FontSize', 8); % 加上子圖標題，設置字體大小為8
    end
    
    saveas(gcf, fullfile(output_path_TCUBA6, [output_file_name, '.png']));    
    
end

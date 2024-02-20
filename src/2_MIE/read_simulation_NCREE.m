clearvars;
clc;

% 輸入和輸出資料夾的路徑
input_path_NCREE = '..\..\data\real_data(V)_七層鋼構架樓層破壞_一階差分'; 
output_path_NCREE = '..\..\result\七層鋼構架樓層破壞_一階差分\MIE';

% 取得資料夾中的所有檔案
file_list = dir(fullfile(input_path_NCREE, '*.dbl.txt'));

% 迴圈遍歷每個檔案
for i = 1:numel(file_list)
    % 取得檔案名稱
    filename = file_list(i).name;
    
    file_path = fullfile(input_path_NCREE, filename);
    [~, name, ~] = fileparts(filename);
    output_filename = sprintf('Mie_%s_20_3_3.txt', name);
    output_path = fullfile(output_path_NCREE, output_filename);
    
    % 調用 mie 函數
    mie(input_path_NCREE, filename, 8, 10, output_path_NCREE, output_filename);
end

%% FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function mie(input_file_path, input_file_name, channel, scale, output_file_path, output_file_name)


    % 讀取輸入（NCREE那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    TotalChannels = textscan(input_file, ' %f %f %f %f %f %f %f %f ');
    
    % 主程式 to_mie.m 位於的資料夾位置
    cd('.\main') 

    output_MIE = zeros(channel, scale); 
   
    % 跑MIE程式（NCREE）
    for i = 1:channel % 這邊要改，自己對應（這邊2跟下面i-1跟7是因為樓地板沒算進去(9601:13600）
        data = transpose(TotalChannels{1, i, 1});    
        output_MIE(i, :) = to_mie(data, scale, 3, 3); 
    end

    % 儲存輸出
    output_file = fopen(fullfile(output_file_path, output_file_name), 'w');
    for i = 1:size(output_MIE, 1)
        fprintf(output_file, '%f ', output_MIE(i, :));
        fprintf(output_file, '\n');
    end
    fclose(output_file);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
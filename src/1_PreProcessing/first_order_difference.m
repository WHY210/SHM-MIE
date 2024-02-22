clearvars;
clc;

% 輸入和輸出資料夾的路徑
input_file_path = "..\..\data\real_data(V)_七層鋼構架樓層破壞_濾波";
output_file_path = "..\..\data\real_data(V)_七層鋼構架樓層破壞_濾波+一階差分";
% 取得資料夾中的所有檔案
file_list = dir(fullfile(input_file_path, '*.txt'));

% 迴圈遍歷每個檔案
for i = 1:numel(file_list)
    filename = file_list(i).name;
    first_order_difference_filter(input_file_path, filename, output_file_path)
end

function first_order_difference_filter(input_file_path, input_file_name, output_file_path)
    output_file_name = input_file_name;
    %{
    % 讀取輸入（TCUBA6那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    TotalChannels = cell(1, 24);
    TotalChannels{1} = textscan(input_file, ' %f ', 'HeaderLines', 10);
    for i = 2:24
        TotalChannels{i} = textscan(input_file, ' %f ', 'HeaderLines', 1);
    end
    fclose(input_file);
    %}
    % 讀取輸入（NCREE那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    TotalChannels = textscan(input_file, ' %f %f %f %f %f %f %f %f ');    
    fclose(input_file);

    diff_data = diff(cell2mat(TotalChannels));

    % 將濾波後的數據存儲為.txt檔案
    output_file = fopen(fullfile(output_file_path, output_file_name), 'w');
    
    % 寫入濾波後的數據
    for i = 1:length(diff_data)
        for channel = 1:8
            fprintf(output_file, '%f\t', diff_data(i, channel));
        end
        fprintf(output_file, '\n');
    end
    
    fclose(output_file);

end

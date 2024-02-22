clearvars;
clc;

% 輸入和輸出資料夾的路徑
input_file_path = "..\..\data\real_data(V)_七層鋼構架樓層破壞_一階差分";
output_file_path = "..\..\data\real_data(V)_七層鋼構架樓層破壞_一階差分+濾波";
% 取得資料夾中的所有檔案
file_list = dir(fullfile(input_file_path, '*.txt'));

% 迴圈遍歷每個檔案
for i = 1:numel(file_list)
    filename = file_list(i).name;
    filterTCUBA6(input_file_path, filename, output_file_path)
end

function filterTCUBA6(input_file_path, input_file_name, output_file_path)
    output_file_name = input_file_name;
    %{
    % 讀取輸入（TCUBA6那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    TotalChannels = cell(1, 24);
    TotalChannels{1} = textscan(input_file, ' %f ', 'HeaderLines', 10);
    min_length = length(TotalChannels{1}{1}); % 最短信號的長度
    for i = 2:24
        TotalChannels{i} = textscan(input_file, ' %f ', 'HeaderLines', 1);
        min_length = min(min_length, length(TotalChannels{i}{1})); % 更新最短信號的長度
    end
    fclose(input_file);
    %}
    % 讀取輸入（NCREE那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    TotalChannels = textscan(input_file, ' %f %f %f %f %f %f %f %f ');
    min_length = length(TotalChannels{1}); % 最短信號的長度
    
    % 設定濾波器參數
    fc = 10; % 截止頻率
    fs = 200; % 取樣頻率
    order = 2;
    
    % 初始化存儲濾波後數據的矩陣
    filtered_data = zeros(min_length, 8);
    
    % 對每個通道進行濾波
    for channel = 1:8
        % 取得該通道的原始信號
        signal = TotalChannels{channel}(1:min_length); % 截斷信號至最短長度
        
        % 設計低通濾波器
        [b, a] = butter(order, fc/(fs/2), 'low');
        
        % 應用濾波器
        filtered_signal = filter(b, a, signal);
        
        % 將濾波後的信號存儲到矩陣中
        filtered_data(:, channel) = filtered_signal;
        
        % 繪製濾波前後的頻譜圖
        figure;
        subplot(2,1,1);
        plot_spectrum(signal, fs, 'before Low-pass filter');
        subplot(2,1,2);
        plot_spectrum(filtered_signal, fs, 'after Low-pass filter');
        sgtitle(sprintf('channel %d', channel));
        % 將圖片保存為png檔案
        saveas(gcf, fullfile(output_file_path, sprintf('%s_channel_%02d_spectrum.png', output_file_name, channel)));
        close(gcf);
    end
    
    % 將濾波後的數據存儲為.txt檔案
    
    output_file = fopen(fullfile(output_file_path, output_file_name), 'w');
    

    % 寫入濾波後的數據
    for i = 1:min_length
        for channel = 1:8
            fprintf(output_file, '%f\t', filtered_data(i, channel));
        end
        fprintf(output_file, '\n');
    end
    
    fclose(output_file);

end

function plot_spectrum(signal, fs, title_str)
    L = length(signal);
    Y = fft(signal);
    P2 = abs(Y/L);
    P1 = P2(1:L/2+1);
    P1(2:end-1) = 2*P1(2:end-1);
    f = fs*(0:(L/2))/L;
    plot(f,P1)
    title(title_str)
    xlabel('frequency (Hz)')
    ylabel('amplitude')
    ylim([0, 0.001])
    %ylim([0, 0.5])
end

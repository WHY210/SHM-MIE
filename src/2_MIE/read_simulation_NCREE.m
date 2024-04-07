clearvars;
clc;

%% VARIABLES %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
scale = 30;
channel = 6;
channels = [2, 8, 11, 14, 17, 20];
input_path_NCREE = '..\..\..\data\TCUBA6_交大公教宿舍_濾波';
output_path_NCREE = sprintf('..\\..\\..\\result\\TCUBA6_交大公教宿舍_濾波_%d_3_3\\MIE', scale);


%% MAIN CODE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 主程式 to_mie.m 位於的資料夾位置
cd('.\main') 
[status, message, messageid] = mkdir(output_path_NCREE);
file_list = dir(fullfile(input_path_NCREE, '*.txt'));
for i = 1:numel(file_list)

    filename = file_list(i).name;
    file_path = fullfile(input_path_NCREE, filename);
    [~, name, ~] = fileparts(filename);
    output_filename = sprintf('%s.txt', name);
    output_path = fullfile(output_path_NCREE, output_filename);
    % 調用 mie 函數
    tic
    mie(input_path_NCREE, filename, channel, scale, output_path_NCREE, output_filename, channels);
    toc
    fprintf(['COMPLETE: ', filename, '\n']);
end

%% FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function mie(input_file_path, input_file_name, channel, scale, output_file_path, output_file_name, channels)

    % 讀取輸入（NCREE那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    TotalChannels = textscan(input_file, ' %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f %f');
    fclose(input_file);

    min_segment_start = zeros(1, channel); % 初始化最小震幅的段落起始索引矩陣
    min_segment_end = zeros(1, channel); % 初始化最小震幅的段落結束索引矩陣
    output_MIE = zeros(channel, scale); 
   
    % 跑MIE程式（NCREE）
    
    for i = 1:channel % 這邊要改，自己對應（這邊2跟下面i-1跟7是因為樓地板沒算進去
        % data = transpose(TotalChannels{2*i-1});     
        data = transpose(TotalChannels{channels(i)});
        %[min_segment, min_segment_start, min_segment_end] = calculate_min_segment(i, data, 4000, min_segment_start, min_segment_end, channels);
        
        min_segment = data(0001:2500); %9601:13600);
        min_segment_start = zeros(1, channel) + 0001; %9601;
        min_segment_end =  zeros(1, channel) + 2500;  %13600;
        
        output_MIE(i, :) = to_mie(min_segment, scale, 3, 3);
    end
    figure('Position', [50, 50, 2000, 800]);
    plot_and_save_figures(TotalChannels, min_segment_start, min_segment_end, output_MIE, channel, channels);
    saveas(gcf, fullfile(output_file_path, [output_file_name, '.png'])); 
    clf;
    output_file = fopen(fullfile(output_file_path, output_file_name), 'w');
    for i = 1:size(output_MIE, 1)
        fprintf(output_file, '%f ', output_MIE(i, :));
        fprintf(output_file, '\n');
    end
    fclose(output_file);
end


function [min_segment, min_segment_start, min_segment_end] = calculate_min_segment(i, data, segment_length, min_segment_start, min_segment_end, channels)
    % 定義時間歷史的起始索引和結束索引
    start_index = 1;
    end_index = segment_length;
    

    min_amplitude = inf;  % 初始化最小震幅為無窮大
    
    while end_index <= length(data)
        % 計算當前段落的震幅
        segment_amplitude = max(abs(data(start_index:end_index)));
        
        % 如果當前段落的震幅比最小震幅還小，則更新最小震幅和段落起始索引
        if segment_amplitude < min_amplitude
            min_amplitude = segment_amplitude;
            min_segment_start(i) = start_index;
        end
        
        % 移動到下一個段落的起始索引
        start_index = start_index + 1;
        end_index = end_index + 1;
    end
    
    % 儲存最小震幅的連續4000點的段落的結束索引
    min_segment_end(i) = min_segment_start(i) + segment_length - 1;
    
    % 得到最小震幅的連續4000點的段落
    min_segment = data(min_segment_start(i):min_segment_end(i));
end


function plot_and_save_figures(TotalChannels, min_segment_start, min_segment_end, output_MIE, channel, channels)
    
    for i = 1:channel
        % 取得第i個通道的資料
        data = transpose(TotalChannels{channels(i)});
        
        % 在subplot中繪製震幅隨時間的變化圖
        subplot(channel, 2, 2*i-1);
        plot(data);
        
        hold on;  
        plot(min_segment_start(i):min_segment_end(i), data(min_segment_start(i):min_segment_end(i)), 'r', 'LineWidth', 1);
        ylim([-0.2 0.2]);
        set(gca, 'XScale', 'linear', 'YScale', 'linear');
        title(['Channel ', num2str(channels(i)-1), 'F'], FontSize=7);
        
        grid on;
        hold off;
    end  

    subplot(channel, 2, [2:2:2*channel]);
    channel_colors = {'red', '#FC9F4D', '#EDB120', '#77AC30', '#0072BD', '#7E2F8E'};
    %channel_colors = {'black', 'red', '#FC9F4D', '#EDB120', '#77AC30', 'blue', '#0072BD', '#7E2F8E'};
    
    for j = 1:channel
        plot(output_MIE(j, :), "o-", 'LineWidth', 1, 'MarkerSize', 1, 'color', channel_colors{j});
        
        hold on;

    end
    ylim([0 4.5]);
    set(gca, 'XScale', 'linear', 'YScale', 'linear');
    legend('B2', '1F', '2F', '3F','7F','14F', 'Location', 'southoutside', 'Orientation', 'horizontal');
    %legend('floor', '1F', '2F', '3F', '4F', '5F', '6F', '7F', 'Location', 'southoutside', 'Orientation', 'horizontal');
    title('MIE for All Channels');
    xlabel('Scale');
    ylabel('MIE');
    grid on;
    
    hold off;
   
    
end

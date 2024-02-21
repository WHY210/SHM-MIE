clearvars;
clc;
profile on

input_path_NCREE = "..\..\data\real_data(V)_七層鋼構架樓層破壞";
output_path_NCREE = "..\..\\result\七層鋼構架樓層破壞";
input_path_TCUBA6 = "..\..\data\TCUBA6_交大公教宿舍";
output_path_TCUBA6 = "..\..\result\TCUBA6_交大公教宿舍";
input_path_TCUBAA = "..\..\data\TCUBAA_交大圖書館";
output_path_TCUBAA = "..\..\result\TCUBAA_交大圖書館";
input_path_SAP2000 = "..\..\data\white\模擬數據";
output_path_SAP2000 = "..\..\result\white\模擬數據";

% 德馨公教大樓
file_numbers = [
    
    94060600, 94091600, 94100500, 94101200, 94102800, 94112600, 95022300, 95032400, 95040300, 95042400, 
    95050200, 95062500, 95071400, 95082000, 95120100, 95121800, 96012200, 96030500, 96030501, 96072900, 
    96112600, 98050300, 98050900, 98071700, 99071100, 99092000, 99092002, 99092003, 99092004, 99092005, 
    99092006, 99092007, 99092008, 99092009, 99092200, 99092201, 99092300, 99092500, 99093000, 99101800, 
    99101801, 01011100, 01022400, 01061300, 01061400, 01063000, 01121800, 02021200, 02033100, 02051500,     
    02052800, 02061400, 02082900, 02090700, 02091600, 03060900, 03061000, 03071800, 03080300, 03081100, 
    04010100, 04020400, 04050100, 04050900, 04051500, 04101300, 04101500, 04110800, 04111100, 05043000, 
    05051700, 05060100, 05072600, 05073100, 05090600, 05091200, 05100500, 05101500, 07072300, 07101100, 
    08060100, 08090900, 08120700, 09071300, 09081700, 09100300, 09100400, 09110500, 09110501, 09111500, 
    09112100, 10010400, 10020700, 10030400, 10042600, 10062600, 10112100, 11043000, 12060900, 12061300, 
    12061301, 12081400, 12083100, 13020200, 13030700, 13032700, 13060200, 13103100, 14022100, 14052100
    
    ];



input_filenames = strcat(num2str(file_numbers'), ".txt"); % matlab會把前面的0去掉==自己加
output_filenames = strcat("Mie_19", num2str(file_numbers'), "_15_3_3.txt"); % 或20

for i = 1:length(file_numbers)
    mie(input_path_TCUBA6, input_filenames{i}, 24, 15, output_path_TCUBA6, output_filenames{i});
    fprintf(input_filenames{i});
    fprintf("   ")
end


%% FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function mie(input_file_path, input_file_name, channel, scale, output_file_path, output_file_name)

    % 讀取輸入（TCUBA6那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    a2 = cell(1, channel);
    a2{1} = textscan(input_file, ' %f ', 'HeaderLines', 10);
    for i = 2:channel
        a2{i} = textscan(input_file, ' %f ', 'HeaderLines', 1);
    end
    %{
    % 讀取輸入（NCREE那種）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    a1 = textscan(input_file, ' %f %f %f %f %f %f %f %f ');
    % 讀取輸入（SPA2000）
    input_file = fopen(fullfile(input_file_path, input_file_name));
    a3 = textscan(input_file,' %f %f %f %f %f %f %f %f ','HeaderLines',17);
    %}

    % 主程式 to_mie.m 位於的資料夾位置
    cd("..\main") 

    output_MIE = zeros(channel, scale); 
    
    % 跑MIE程式（TCUBA6）
    d2 = cell(channel, 1);
    for i = 1:channel
        d2{i} = transpose(cell2mat(a2{i}));
        output_MIE(i , :) = to_mie(d2{i}(0001:2500), scale, 3, 3); 
    end

    %{
    % 跑MIE程式（NCREE）
    for i = 2:channel % 這邊要改，自己對應（這邊是因為樓地板沒算進去）
        d1 = transpose(a1{1, i, 1});
        output_MIE(i - 1, :) = to_mie(d1(9601:13600), 7, 3, 3); 
    end

    % 跑MIE程式（SAP2000）
    for i = 2:channel % 這邊要改，自己對應（這邊是因為樓地板沒算進去）
        d3 = transpose(a1{1, i, 1});
        output_MIE(i - 1, :) = to_mie(d3(9601:13600), 7, 3, 3); 
    end
    %}

    % 儲存輸出
    output_file = fopen(fullfile(output_file_path, output_file_name), 'w');
    for i = 1:size(output_MIE, 1)
        fprintf(output_file, '%f ', output_MIE(i, :));
        fprintf(output_file, '\n');
    end
    fclose(output_file);
end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clearvars;
clc;

input_path_TCUBA6 = "..\..\result\TCUBA6_交大公教宿舍\DI";
output_path_TCUBA6 = "..\..\result\TCUBA6_交大公教宿舍\DI_plot";

file_numbers = [
    1994060600, 1994091600, 
    %{
    1994100500, 1994101200, 1994102800, 1994112600, 1995022300, 1995032400, 1995040300, 1995042400, ...
    1995050200, 1995062500, 1995071400, 1995082000, 1995120100, 1995121800, 1996012200, 1996030500, 1996030501, 1996072900, ...
    1996112600, 1998050300, 1998050900, 1998071700, 1999071100, 1999092000, 1999092002, 1999092003, 1999092004, 1999092005, ...
    1999092006, 1999092007, 1999092008, 1999092009, 1999092200, 1999092201, 1999092300, 1999092500, 1999093000, 1999101800, ...
    1999101801, 2001011100, 2001022400, 2001061300, 2001061400, 2001063000, 2001121800, 2002021200, 2002033100, 2002051500, ...
    2002052800, 2002061400, 2002082900, 2002090700, 2002091600, 2003060900, 2003061000, 2003071800, 2003080300, 2003081100, ...
    2004010100, 2004020400, 2004050100, 2004050900, 2004051500, 2004101300, 2004101500, 2004110800, 2004111100, 2005043000, ...
    2005051700, 2005060100, 2005072600, 2005073100, 2005090600, 2005091200, 2005100500, 2005101500, 2007072300, 2007101100, ...
    2008060100, 2008090900, 2008120700, 2009071300, 2009081700, 2009100300, 2009100400, 2009110500, 2009110501, 2009111500, ...
    2009112100, 2010010400, 2010020700, 2010030400, 2010042600, 2010062600, 2010112100, 2011043000, 2012060900, 2012061300, ...
    2012061301, 2012081400, 2012083100, 2013020200, 2013030700, 2013032700, 2013060200, 2013103100, 2014022100, 2014052100
    %}
    ];

input_filenames = strcat("DI_", num2str(file_numbers'), ".txt"); 
output_filenames = strcat("DI_", num2str(file_numbers'));

for i = 1:length(file_numbers)
    DI_plot(input_path_TCUBA6, input_filenames{i}, 24, 15, output_path_TCUBA6, output_filenames{i})
    fprintf(input_filenames{i});
    fprintf(" \n")
end

function DI_plot(input_file_path, input_file_name, channel, scale, output_file_path, output_file_name)

% 讀取數據
data = load(fullfile(input_file_path, input_file_name));

% 使用 meshgrid 生成網格
x = 1:channel;
y = 1:scale;
[X, Y] = meshgrid(x, y);


%{
% 由於您的數據是一個一維數組，需要將其變形為與網格相對應的矩陣
data_matrix = reshape(data, scale, channel)';

% 繪製三維散點圖
figure;
scatter3(X(:), Y(:), data_matrix(:), 'o');
grid on;
%}


% 由於您的數據是一個一維數組，需要將其變形為與網格相對應的矩陣
data_matrix = reshape(data, channel, scale)';

% 繪製三維表面
figure;
surf(X, Y, data_matrix, 'EdgeColor', 'none', 'FaceColor', 'interp');
colorbar;  % 顯示顏色條
clim([-3,3]);



% 設置標籤
xlabel('channel');
ylabel('scale');
zlabel('DI（未相加）');

xticks(1:channel);
yticks(1:scale);
zticks(-3:3);

% 顯示圖形
output_file_name = strrep(output_file_name, '_', '-');
title(output_file_name, fontsize=13);
axis equal;  % 使坐標軸比例相等
view(3);  % 設置視圖為三維

% 保存圖片
saveas(gcf, fullfile(output_file_path, [output_file_name, '.jpg']));


end

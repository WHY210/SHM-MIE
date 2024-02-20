clearvars;
clc;

input_path_TCUBA6 = "D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍\MIE";
output_path_TCUBA6 = "D:\0005_大專生計畫\04_MIE\result\TCUBA6_交大公教宿舍\DI";

input_path_NCREE = "D:\0005_大專生計畫\04_MIE\result\七層鋼構架樓層破壞\MIE";
output_path_NCREE = "D:\0005_大專生計畫\04_MIE\result\七層鋼構架樓層破壞\DI";

% 取得資料夾中的所有檔案
file_list = dir(fullfile(input_path_NCREE, '*.txt'));

% 迴圈遍歷每個檔案
for i = 1:numel(file_list)
    % 取得檔案名稱
    filename = file_list(i).name;
    
    file_path = fullfile(input_path_NCREE, filename);
    [~, name, ~] = fileparts(filename);
    output_filename = sprintf('DI_%s.txt', name);
    output_path = fullfile(output_path_NCREE, output_filename);
    
    DI(input_path_NCREE, filename, output_path_NCREE, output_filename)
end

%{
file_numbers = [
    1994060600, 1994091600, 1994100500, 1994101200, 1994102800, 1994112600, 1995022300, 1995032400, 1995040300, 1995042400, ...
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
    ];

input_filenames = strcat("Mie_", num2str(file_numbers'), "_15_3_3.txt"); 
output_filenames = strcat("DI_", num2str(file_numbers'), ".txt");

for i = 1:length(file_numbers)
    DI(input_path_TCUBA6, input_filenames{i}, output_path_TCUBA6, output_filenames{i})
    fprintf(input_filenames{i});
    fprintf(" \n")
end
%}

%% FUNCTION %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function DI(input_file_path, input_file_name, output_file_path, output_file_name)
    
cd("D:\0005_大專生計畫\04_MIE\result\七層鋼構架樓層破壞\MIE")
    UD001 = load('.\\Mie_UD001_7_3_3.txt');
    UD01  = load('.\\Mie_UD01_7_3_3.txt');
    UD002 = load('.\\Mie_UD002_7_3_3.txt');
    UD02  = load('.\\Mie_UD02_7_3_3.txt');
    UD003 = load('.\\Mie_UD003_7_3_3.txt');
    UD03  = load('.\\Mie_UD03_7_3_3.txt');
    UD04  = load('.\\Mie_UD04_7_3_3.txt');
    
    reference = (UD001+UD01+UD002+UD02+UD003+UD03+UD04)./7;
    
    %reference = load(fullfile(input_file_path, "Mie_1994060600_15_3_3.txt"));
    evaluate = load(fullfile(input_file_path, input_file_name));
    
    damage_index = evaluate - reference;

    output_file = fopen(fullfile(output_file_path, output_file_name), 'w');
    for i = 1:size(damage_index, 1)
        fprintf(output_file, '%f ', damage_index(i, :));
        fprintf(output_file, '\n');
    end
    fclose(output_file);  

end


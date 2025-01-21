% encoding:GB 2312
%% 房屋信息提取
% 读取文件并解析
clc;

if false
    data_file = '../test-1.txt';
    [file_id, ~] = fopen(data_file, 'r');
    origin_data = cell(0);

    while ~feof(file_id)
        cur_line = fgetl(file_id);
        disp(cur_line);
        origin_data{length(origin_data) + 1, 1} = cur_line;
    end

    fclose(file_id);

    % 排除第一行标签名
    data = table();

    for k = 2:length(origin_data)
        t_size = size(data);
        cur_line = origin_data{k, 1};
        split_line = split(cur_line, ',');
        data.district(t_size(1) + 1) = string(split_line{1});
        data.name(t_size(1) + 1) = string(split_line{2});
        data.certificate_no(t_size(1) + 1) = string(split_line{3});
        data.pre_sale_scope(t_size(1) + 1) = string(split_line{4});
        data.number_of_house(t_size(1) + 1) = str2double(split_line{5});
        data.start_datatime(t_size(1) + 1) = datetime(split_line{7}, 'InputFormat', 'yyyy-MM-dd');
        data.house_location(t_size(1) + 1) = string(split_line{end});
    end

    data_test = data;
else
    load('data.mat');
    data_test = data;
end

clearvars -except data_test ;
%% data mining -1 不同区域小区数对比
clc;
village_qy = data_test(strcmpi(data_test.district, "青羊区"), :);
village_jj = data_test(strcmpi(data_test.district, "锦江区"), :);
village_jn = data_test(strcmpi(data_test.district, "金牛区"), :);
village_wh = data_test(strcmpi(data_test.district, "武侯区"), :);
village_ch = data_test(strcmpi(data_test.district, "成华区"), :);
village_sl = data_test(strcmpi(data_test.district, "双流区"), :);
village_tf = data_test(strcmpi(data_test.district, "天府新区"), :);
village_gxn = data_test(strcmpi(data_test.district, "高新南区"), :);
village_pd = data_test(strcmpi(data_test.district, "郫都区"), :);
village_xd = data_test(strcmpi(data_test.district, "新都区"), :);
village_wj = data_test(strcmpi(data_test.district, "温江区"), :);
% village_lqy = data_test(strcmpi(data_test.district, "龙泉驿"), :);
% village_pz = data_test(strcmpi(data_test.district, "彭州市"), :);
% village_djy = data_test(strcmpi(data_test.district, "都江堰市"), :);
% village_pj = data_test(strcmpi(data_test.district, "浦江县"), :);
% village_jy = data_test(strcmpi(data_test.district, "简阳市"), :);

vallage_name = {'青羊区', '锦江区', '金牛区', '武侯区', '成华区', ...
                '双流区', '天府新区', '高新南区', '郫都区', '新都区', ...
                '温江区'};
village_district = {village_qy, village_jj, village_jn, village_wh, village_ch, ...
                        village_sl, village_tf, village_gxn, village_pd, village_xd, ...
                        village_wj};
district_village_num = zeros(0); % 小区数目
district_house_num = zeros(0); % 套数

for k = 1:length(village_district)
    cur_village = village_district{k};
    district_village_num(k) = height(cur_village);
    district_house_num(k) = sum(cur_village.number_of_house);
end

%%
tcf('district village'); figure('Name', 'district village', 'Color', 'w');
subplot(211)
bar(district_village_num);
xticks(linspace(1, 11, 11));
xticklabels(vallage_name);
grid('minor');
xlabel('区(县)'); ylabel('小区数量'); title('所有时间段不同区(县)小区数');

subplot(212)
bar(district_house_num);
xticks(linspace(1, 11, 11));
xticklabels(vallage_name);
grid('minor');
xlabel('区(县)'); ylabel('房子数量/套'); title('所有时间段不同区(县)房子数');

% encoding:GB 2312
%% ������Ϣ��ȡ
% ��ȡ�ļ�������
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

    % �ų���һ�б�ǩ��
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
%% data mining -1 ��ͬ����С�����Ա�
clc;
village_qy = data_test(strcmpi(data_test.district, "������"), :);
village_jj = data_test(strcmpi(data_test.district, "������"), :);
village_jn = data_test(strcmpi(data_test.district, "��ţ��"), :);
village_wh = data_test(strcmpi(data_test.district, "�����"), :);
village_ch = data_test(strcmpi(data_test.district, "�ɻ���"), :);
village_sl = data_test(strcmpi(data_test.district, "˫����"), :);
village_tf = data_test(strcmpi(data_test.district, "�츮����"), :);
village_gxn = data_test(strcmpi(data_test.district, "��������"), :);
village_pd = data_test(strcmpi(data_test.district, "ۯ����"), :);
village_xd = data_test(strcmpi(data_test.district, "�¶���"), :);
village_wj = data_test(strcmpi(data_test.district, "�½���"), :);
% village_lqy = data_test(strcmpi(data_test.district, "��Ȫ��"), :);
% village_pz = data_test(strcmpi(data_test.district, "������"), :);
% village_djy = data_test(strcmpi(data_test.district, "��������"), :);
% village_pj = data_test(strcmpi(data_test.district, "�ֽ���"), :);
% village_jy = data_test(strcmpi(data_test.district, "������"), :);

vallage_name = {'������', '������', '��ţ��', '�����', '�ɻ���', ...
                '˫����', '�츮����', '��������', 'ۯ����', '�¶���', ...
                '�½���'};
village_district = {village_qy, village_jj, village_jn, village_wh, village_ch, ...
                        village_sl, village_tf, village_gxn, village_pd, village_xd, ...
                        village_wj};
district_village_num = zeros(0); % С����Ŀ
district_house_num = zeros(0); % ����

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
xlabel('��(��)'); ylabel('С������'); title('����ʱ��β�ͬ��(��)С����');

subplot(212)
bar(district_house_num);
xticks(linspace(1, 11, 11));
xticklabels(vallage_name);
grid('minor');
xlabel('��(��)'); ylabel('��������/��'); title('����ʱ��β�ͬ��(��)������');

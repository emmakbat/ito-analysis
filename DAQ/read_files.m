files = dir('/home/emmabat/Programming/Python/ito-analysis/DAQ/*.mat');

peak_heights = {};
equilibrium_potentials = {};
labels = {};

for i=1:length(files) 
    output = load(files(i).name); 
    data_names = string(fieldnames(output));
    output_cell = struct2cell(output);
    for j=1:length(output_cell)
        labels = [labels, data_names{j}];
        timedata = output_cell{j};
        plot(timedata.Time, timedata{:, 1})
        saveas(gcf, strcat(data_names{j}, '.png'))
        
        S = seconds(timedata.Time);
        
        % min(timedata{:, 1} should give height of nucleation peak  
        peak_heights = [peak_heights, min(timedata{:, 1})];
        
        dydx = diff(timedata{:, 1})./diff(S);
        find_zero_index = @(v) find(diff(sign(v)));
        zeros =  find_zero_index(dydx);
        
        equilibrium_potentials = [equilibrium_potentials, timedata{zeros(ceil(end/2)), 1}];
    end
end
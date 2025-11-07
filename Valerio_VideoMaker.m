close all
clear all
clc

%%

titlename = 'Video title here';
ylB = [-1.5,2];
load('directorynames/Experiment_Analysis.mat','CellPos','time');

nreplicate = 3;

movie_output = 'VideoFileNameHere';
myfps = 15; % write fps

%% Don't change
writerObj = VideoWriter(movie_dir, 'MPEG-4');
writerObj.FrameRate = myfps;
open(writerObj);
%%

fh = figure;
set(fh,'color','white');
xl = [0,1]; yl = [0,0.9];

xlim(xl); ylim(yl); box on; hold on;
xlabel('X, mm'); ylabel('Y, mm'); set(gca,'YDir','reverse');
daspect([1,1,1]);

for i = 1:length(time)

    posdata = CellPos{nreplicate,i}.*pixtomm;
    hold on;
    p = plot(posdata(:,1),posdata(:,2),'k.','markersize',8);
    title([sprintf('%03d',floor(time(i)*60)),'s'])
    pause(0.1);

    F = getframe(gcf);
    writeVideo(writerObj,F);
    hold off
    delete(p);


end

close(gcf);
close(writerObj);
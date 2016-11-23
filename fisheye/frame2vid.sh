
for i in {1..9}
do
  mv "frame-$i.png" "frame-0$i.png";
done

ffmpeg -f image2 -r 3 -i frame-%02d.png -vcodec mpeg4 -y movie.mp4

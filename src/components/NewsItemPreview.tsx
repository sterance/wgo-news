import { Stack, Typography, Link } from "@mui/material";
import "../components/NewsItemPreview.css";

export default function NewsItemPreview() {
  return (
    <Stack>
      <Typography variant="h4">
        <Link href="#" target="_blank" rel="noopener">
          Example News Story Title
        </Link>
      </Typography>
      <div className="news-preview-body">
        <Typography variant="body1" className="truncated-body">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis dolor mi, pellentesque quis dictum sed, laoreet sed purus. Etiam condimentum quis ipsum vitae volutpat. Donec ac euismod lacus. Phasellus luctus nulla ex. Curabitur et venenatis dui, sit amet maximus tellus. Proin sit amet eleifend ipsum. Etiam ornare, ante non efficitur facilisis, justo turpis condimentum sapien, eget auctor tortor enim et nisi. Duis cursus, neque nec semper aliquet, nibh tellus posuere erat, sit amet lacinia ligula erat a metus. Morbi at lacinia augue. Suspendisse arcu mauris, elementum sed rutrum ac, vulputate eleifend purus. Ut interdum eget nunc nec dictum. Aliquam at tempus magna. Sed et enim commodo, vehicula massa et, dignissim ligula. Curabitur eget eros diam. Quisque dapibus enim ut porttitor vehicula. Mauris porttitor mollis facilisis. Duis quis massa est. Vestibulum felis leo, malesuada quis magna eu, sodales congue tortor. Mauris hendrerit dolor sed eros egestas mollis. Duis pulvinar, massa hendrerit iaculis porttitor, dolor lectus luctus augue, id aliquam leo magna ultrices nulla. Etiam sit amet elit aliquam, lacinia dui ac, eleifend tellus. Vivamus nisl lorem, posuere a iaculis id, vulputate quis tortor. Nam molestie vel odio vitae consectetur. Phasellus vehicula ligula in facilisis fermentum. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Integer in congue lacus. Integer arcu nulla, dictum ut urna eget, tincidunt elementum augue. Sed eleifend eget elit mattis efficitur. Ut at euismod metus. Donec blandit, diam eget ullamcorper faucibus, urna lacus ultrices tellus, non gravida odio magna eget neque. Aliquam vulputate volutpat dolor ac semper. Vestibulum augue quam, lobortis id ornare vel, varius cursus erat. Morbi vel velit id purus placerat fringilla nec pharetra risus. Integer eu dui ac enim accumsan condimentum. Cras lectus orci, dignissim vitae lectus eu, bibendum sagittis eros. Praesent pharetra, tortor a vulputate hendrerit, enim mauris euismod orci, a sodales enim elit ac quam. Duis neque elit, maximus in velit et, malesuada tempor tortor. Quisque aliquet aliquet porta. Aenean ac erat justo. Nulla porttitor urna orci, vitae lobortis leo molestie non. Nam dictum eleifend egestas. Aliquam lobortis mi non nulla tempor, id sodales diam sagittis. Vestibulum faucibus ex nisl, sit amet auctor lectus consequat eget. Nunc libero leo, blandit vitae urna ut, fringilla commodo metus. Curabitur maximus sodales convallis. Duis eleifend augue a augue eleifend imperdiet.
        </Typography>
        <Link href="#" className="read-more-link">
          Read More...
        </Link>
      </div>
    </Stack>
  );
}

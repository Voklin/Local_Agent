"""Render the source SVG into PNG and a multi-resolution Windows icon."""
from pathlib import Path
from PySide6.QtCore import QRectF,QBuffer,QIODevice,Qt,QByteArray
from PySide6.QtGui import QImage,QPainter
from PySide6.QtSvg import QSvgRenderer
import struct


def main():
    root=Path(__file__).resolve().parents[1]
    target=root/'assets'
    # Derive the app icon from the same silhouette, on a stable contrasting tile.
    svg=(target/'leshy.svg').read_text(encoding='utf-8').replace('fill="currentColor"','fill="#eed6a7"')
    svg=svg.replace('<path','<rect width="100" height="96" rx="18" fill="#20261d"/><g transform="translate(10 10) scale(.8)"><path').replace('</svg>','</g></svg>')
    renderer=QSvgRenderer(QByteArray(svg.encode('utf-8')))
    if not renderer.isValid():raise ValueError('Invalid LESHY SVG')
    image=QImage(512,512,QImage.Format.Format_ARGB32)
    image.fill(0)
    painter=QPainter(image);painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    renderer.render(painter,QRectF(0,0,512,512));painter.end()
    image.save(str(target/'leshy.png'))
    sizes=[16,24,32,48,64,128,256];frames=[];entries=[];offset=6+16*len(sizes)
    for size in sizes:
        buffer=QBuffer();buffer.open(QIODevice.OpenModeFlag.WriteOnly)
        image.scaled(size,size,Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation).save(buffer,'PNG')
        data=bytes(buffer.data());frames.append(data)
        entries.append(struct.pack('<BBBBHHII',size%256,size%256,0,0,1,32,len(data),offset));offset+=len(data)
    (target/'leshy.ico').write_bytes(struct.pack('<HHH',0,1,len(sizes))+b''.join(entries)+b''.join(frames))


if __name__=='__main__':main()

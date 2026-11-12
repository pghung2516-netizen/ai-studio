import React, {useEffect, useState} from 'react';
import {
  AbsoluteFill,
  Easing,
  Img,
  continueRender,
  delayRender,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from 'remotion';

export type ProductCardProps = {
  name: string;
  price: string;
  oldPrice?: string;
  cta: string;
  tagline?: string;
  shopName?: string;
  image?: string; // tên file trong public/imgs/ (script batch tự chép vào)
  colorMain: string;
  colorBg: string;
  colorText: string;
};

const FONT = 'BeVietnamPro';

// Nạp font Be Vietnam Pro từ public/fonts (chép từ assets/fonts của workspace)
const useFonts = () => {
  const [handle] = useState(() => delayRender('Nạp font Be Vietnam Pro'));
  useEffect(() => {
    const weights: [string, string][] = [
      ['400', 'BeVietnamPro-Regular.ttf'],
      ['600', 'BeVietnamPro-SemiBold.ttf'],
      ['700', 'BeVietnamPro-Bold.ttf'],
      ['800', 'BeVietnamPro-ExtraBold.ttf'],
    ];
    Promise.all(
      weights.map(async ([weight, file]) => {
        const face = new FontFace(FONT, `url(${staticFile('fonts/' + file)})`, {weight});
        await face.load();
        document.fonts.add(face);
      }),
    )
      .then(() => continueRender(handle))
      .catch((e) => {
        console.error(e);
        continueRender(handle);
      });
  }, [handle]);
};

const ease = Easing.bezier(0.16, 1, 0.3, 1);

export const ProductCard: React.FC<ProductCardProps> = (p) => {
  useFonts();
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();

  const appear = (start: number, dist = 60) => ({
    opacity: interpolate(frame, [start, start + 15], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    }),
    translate: `0px ${interpolate(frame, [start, start + 20], [dist, 0], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: ease,
    })}px`,
  });

  const imgScale = spring({frame, fps, config: {damping: 200}, durationInFrames: 40});
  const imgZoom = interpolate(frame, [0, 180], [1, 1.08]);
  const ctaPulse = 1 + 0.04 * Math.sin((frame / fps) * Math.PI * 2 * 1.2);
  const ctaIn = spring({frame: frame - 100, fps, config: {damping: 12}});

  return (
    <AbsoluteFill style={{backgroundColor: p.colorBg, fontFamily: FONT, color: p.colorText}}>
      {/* Dải màu trên cùng */}
      <div style={{position: 'absolute', top: 0, left: 0, right: 0, height: 24, background: p.colorMain}} />

      {/* Tên shop */}
      <div
        style={{
          position: 'absolute', top: 90, left: 0, right: 0, textAlign: 'center',
          fontSize: 44, fontWeight: 700, letterSpacing: 2, color: p.colorMain,
          ...appear(0, -30),
        }}
      >
        {p.shopName}
      </div>

      {/* Ảnh sản phẩm */}
      <div
        style={{
          position: 'absolute', top: 190, left: 110, width: 860, height: 860,
          borderRadius: 48, overflow: 'hidden', background: '#fff',
          boxShadow: '0 30px 80px rgba(0,0,0,0.18)',
          scale: String(0.8 + 0.2 * imgScale),
          opacity: imgScale,
        }}
      >
        {p.image ? (
          <Img
            src={staticFile('imgs/' + p.image)}
            style={{width: '100%', height: '100%', objectFit: 'cover', scale: String(imgZoom)}}
          />
        ) : (
          <div
            style={{
              width: '100%', height: '100%', display: 'flex', alignItems: 'center',
              justifyContent: 'center', fontSize: 64, fontWeight: 700, color: p.colorMain,
              background: `linear-gradient(135deg, ${p.colorBg}, #fff)`,
            }}
          >
            Ảnh sản phẩm
          </div>
        )}
      </div>

      {/* Tên sản phẩm */}
      <div
        style={{
          position: 'absolute', top: 1090, left: 80, right: 80, textAlign: 'center',
          fontSize: 76, fontWeight: 800, lineHeight: 1.2,
          ...appear(25),
        }}
      >
        {p.name}
      </div>

      {p.tagline ? (
        <div
          style={{
            position: 'absolute', top: 1310, left: 80, right: 80, textAlign: 'center',
            fontSize: 44, fontWeight: 400, opacity: 0.75,
            ...appear(40, 40),
          }}
        >
          {p.tagline}
        </div>
      ) : null}

      {/* Giá */}
      <div
        style={{
          position: 'absolute', top: 1400, left: 0, right: 0, textAlign: 'center',
          ...appear(55),
        }}
      >
        {p.oldPrice ? (
          <span style={{fontSize: 48, fontWeight: 600, textDecoration: 'line-through', opacity: 0.5, marginRight: 28}}>
            {p.oldPrice}
          </span>
        ) : null}
        <span style={{fontSize: 120, fontWeight: 800, color: p.colorMain}}>{p.price}</span>
      </div>

      {/* Nút kêu gọi */}
      <div
        style={{
          position: 'absolute', top: 1620, left: 190, right: 190, height: 150,
          borderRadius: 75, background: p.colorMain, color: '#fff',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 72, fontWeight: 800,
          boxShadow: `0 16px 40px ${p.colorMain}88`,
          scale: String(Math.max(0, ctaIn) * ctaPulse),
        }}
      >
        {p.cta}
      </div>
    </AbsoluteFill>
  );
};

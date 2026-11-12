import React from 'react';
import {Composition} from 'remotion';
import {ProductCard, ProductCardProps} from './ProductCard';

// Giá trị mặc định - bị ghi đè bởi --props hoặc dữ liệu trong scripts/render-batch.mjs
const defaultProps: ProductCardProps = {
  name: 'Áo thun cotton basic',
  price: '199.000đ',
  oldPrice: '299.000đ',
  cta: 'Mua ngay',
  tagline: 'Mềm mát - Form chuẩn',
  shopName: 'Shop Mẫu',
  image: '',
  colorMain: '#FF6B35',
  colorBg: '#FFF4EC',
  colorText: '#1F1F1F',
};

export const Root: React.FC = () => (
  <Composition
    id="ProductCard"
    component={ProductCard}
    durationInFrames={180} // 6 giây x 30 fps
    fps={30}
    width={1080}
    height={1920}
    defaultProps={defaultProps}
  />
);

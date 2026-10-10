# Stellar Pathfinder Brand Assets

Professional logo and branding assets for Stellar Pathfinder.

## Logo Files

### `logo.svg` - Icon Only (400x400)
- **Use for**: App icons, favicons, social media profile pictures
- **Format**: Square icon with star and pathfinding visualization
- **Colors**: Stellar Cyan (#00D1FF), Deep Blue (#0A2540), Success Green (#00C896)

### `logo-with-text.svg` - Full Logo (600x200)
- **Use for**: Website headers, documentation, presentations
- **Format**: Icon + "STELLAR PATHFINDER" text with tagline
- **Layout**: Horizontal orientation

### `icon.svg` - Favicon (128x128)
- **Use for**: Browser favicons, app icons, small displays
- **Format**: Compact square with rounded corners
- **Background**: Gradient (Deep Blue to Brand Blue)

### `banner.svg` - Social Preview (1280x640)
- **Use for**: GitHub social preview, Twitter cards, LinkedIn shares
- **Format**: Wide banner with logo, title, and tagline
- **Optimized for**: Social media OG images

## Design Elements

### Core Symbol
- **Stellar Star**: Represents the Stellar network with radiating rays
- **Pathfinding Routes**: Multiple curved and straight paths showing:
  - **Solid cyan line**: Best/direct route (GOOD verdict)
  - **Dashed green line**: Alternative good route (FAIR verdict)
  - **Faded orange line**: Poor route (warning)
- **Network Nodes**: Connection points representing liquidity sources

### Color Palette

| Color | Hex | Usage |
|-------|-----|-------|
| Deep Blue | `#0A2540` | Primary brand, backgrounds |
| Stellar Cyan | `#00D1FF` | Accent, highlights, star |
| Brand Blue | `#1E40AF` | Gradients, secondary |
| Success Green | `#00C896` | Good routes, positive indicators |
| Warning Amber | `#F59E0B` | Poor routes, warnings |
| Pure White | `#FFFFFF` | Star center, text on dark |

### Typography
- **Font**: Arial, sans-serif (for universal compatibility)
- **Title**: 800 weight, tight letter-spacing (-1.5px)
- **Tagline**: 400 weight, normal letter-spacing

## Usage Guidelines

### ✅ Do
- Use SVG format for web and digital displays (scalable, high quality)
- Maintain aspect ratios when resizing
- Use on dark or brand-colored backgrounds for best contrast
- Preserve gradients and transparency

### ❌ Don't
- Don't stretch or distort the logo
- Don't change the color palette
- Don't add effects (shadows, outlines) to the SVG
- Don't use on busy photographic backgrounds

## Implementation

### GitHub Repository
Add `banner.svg` as the social preview image:
1. Repository Settings → General
2. Scroll to "Social Preview"
3. Upload `assets/banner.svg`

### Website Favicon
```html
<link rel="icon" type="image/svg+xml" href="/assets/icon.svg">
```

### README Header (from this directory)
```markdown
![Stellar Pathfinder](banner.svg)
```

### Open Graph Meta Tags
```html
<meta property="og:image" content="https://stellar-pathfinder.onrender.com/assets/banner.svg">
<meta property="og:image:width" content="1280">
<meta property="og:image:height" content="640">
```

## File Formats

All logos are provided in SVG (Scalable Vector Graphics) format:
- ✅ **Scalable**: Looks perfect at any size
- ✅ **Lightweight**: Small file sizes
- ✅ **Editable**: Can be customized if needed
- ✅ **Web-optimized**: Works in all modern browsers

## License

These brand assets are part of the Stellar Pathfinder project and are licensed under Apache-2.0.

---

**Created with**: SVG + Stellar brand colors
**Symbolism**: Star (Stellar) + Paths (Corridor monitoring) + Network nodes (Liquidity)
**Design theme**: Modern fintech aesthetic

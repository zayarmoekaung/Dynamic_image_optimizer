# Dynamic_image_optimizer
Light Weight Dynamic Image Optimizer using Python 
# Image Optimization API

This API provides a single endpoint to fetch, optimize, and serve images dynamically based on client device characteristics. It supports resizing for device dimensions, Device Pixel Ratio (DPR), and format negotiation (WebP or JPEG). Optimized images are cached to improve performance for subsequent requests.

## Base URL
- `/optimize` 

## Authentication
- None required for now (public endpoint).

## Endpoint: Optimize Image
### GET /optimize
Fetches an external image, optimizes it based on device type and client parameters, and returns the optimized image. Supports caching for performance.

#### Query Parameters
| Parameter | Type   | Required | Description | Example |
|-----------|--------|----------|-------------|---------|
| `url`     | String | Yes      | URL of the image to optimize (must start with `http://` or `https://`). | `https://example.com/image.jpg` |
| `width`   | Integer | No       | Client viewport width (px). Overrides device defaults. | `375` |
| `height`  | Integer | No       | Client viewport height (px). Overrides device defaults. | `812` |
| `dpr`     | Float   | No       | Device Pixel Ratio for high-res displays. Defaults to 1.0. | `2.0` |

#### Headers
| Header     | Description | Example |
|------------|-------------|---------|
| `User-Agent` | Used to detect device type (mobile, tablet, desktop). | `Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)` |
| `Accept`     | Preferred image format. Supports `image/webp`,`image/png`,`image/bmp`,`image/gif`,`image/tiff`, or `image/jpeg`. | `image/webp,image/jpeg` |

#### Device Optimization Rules
- **Desktop**: Max 1920x1080, quality 85.
- **Tablet**: Max 1024x768, quality 75.
- **Mobile**: Max 640x480, quality 65.
- **Comic Strips** (aspect ratio > 3): Width-driven resize, max height 8000px (for long ahh strips), quality 90.

#### Responses
| Status | Description | Content-Type | Body |
|--------|-------------|--------------|------|
| 200 OK | Optimized image served (from cache or newly processed). | `image/webp` or `image/jpeg` | Binary image data |
| 400 Bad Request | Missing/invalid `url`, `width`, `height`, or `dpr`. | `application/json` | `{"description": "Invalid URL"}` |
| 500 Internal Server Error | Failed to fetch or process image. | `application/json` | `{"description": "Failed to fetch image: <error>"}` |

#### Example Requests
1. **Basic Request (Mobile, WebP)**:
   ```bash
   curl -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3)" \
        -H "Accept: image/webp" \
        "{base_url}/optimize?url=https://example.com/image.jpg"
   ```
   - Returns: WebP image, resized to max 640x480, quality 65.

2. **With Client Dimensions (High-DPI Device)**:
   ```bash
   curl -H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3)" \
        -H "Accept: image/jpeg" \
        "{base_url}/optimize?url=https://example.com/comic.jpg&width=375&height=812&dpr=3"
   ```
   - Returns: JPEG image, width ~1125px (375*3), height proportional (capped at 8000px), quality 90 (if comic strip).

#### Notes
- **Comic Strips**: Tall images (height/width > 3) are resized based on width to preserve quality, with a max height of 8000px.
- **Performance**: Use retries (3 attempts) and timeout (30s) for fetching external images to handle network issues.
- **Client-Side Usage**: Pass `window.innerWidth`, `window.innerHeight`, and `window.devicePixelRatio` in JavaScript for optimal results:
  ```javascript
  const imgUrl = 'https://example.com/image.jpg';
  const optimizeUrl = `/optimize?url=${encodeURIComponent(imgUrl)}&width=${window.innerWidth}&height=${window.innerHeight}&dpr=${window.devicePixelRatio}`;
  ```

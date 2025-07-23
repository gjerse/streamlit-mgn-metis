import numpy as np
from astropy.io import fits
import io
import zipfile
from matplotlib import pyplot as plt

def apply_solar_mask(image, center, radius):
    Y, X = np.ogrid[:image.shape[0], :image.shape[1]]
    dist = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    masked = image.copy()
    masked[dist < radius] = np.nan
    return masked

def save_to_fits_png(image):
    # FITS
    hdu = fits.PrimaryHDU(data=image.astype(np.float32))
    fits_buffer = io.BytesIO()
    hdu.writeto(fits_buffer)
    fits_buffer.seek(0)

    # PNG
    fig, ax = plt.subplots(figsize=(6,6))
    ax.imshow(image, cmap='gray', origin='lower')
    ax.axis('off')
    png_buffer = io.BytesIO()
    fig.savefig(png_buffer, format='png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    png_buffer.seek(0)

    # Zip
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        z.writestr("mgn_output.fits", fits_buffer.read())
        z.writestr("mgn_output.png", png_buffer.read())
    zip_buffer.seek(0)
    return zip_buffer

import os
import math
import errno
import random
import argparse
from PIL import Image
import plotly.graph_objects as go


# Determines if centroids have converged or not by checking if they are
# identical. Absolute convergence may not be reached so you may want to set
# a max number of iterations or increase the tolerance for what is identical.
def converged(centroids, old_centroids):
    if len(old_centroids) == 0:
        return False
    for i in range(len(centroids)):
        if centroids[i] != old_centroids[i]:
            return False
    return True


# Determines the closest centroid to a given pixel.
def get_min(pixel, centroids):
    min_dist = 9999
    min_index = 0

    for i in range(len(centroids)):
        d = math.sqrt((centroids[i][0] - pixel[0])**2
                      + (centroids[i][1] - pixel[1])**2
                      + (centroids[i][2] - pixel[2])**2)
        if d < min_dist:
            min_dist = d
            min_index = i

    return min_index


# Iterates through each pixel and clusters them with the closest centroid.
def cluster_pixels(im, centroids):
    pixels = im.load()
    clusters = [[] for i in range(len(centroids))]

    for x in range(im.width):
        for y in range(im.height):
            min_index = get_min(pixels[x, y], centroids)
            clusters[min_index].append(pixels[x, y])

    return clusters


# Computes new centroids based on the resulting clusters by computing the mean.
def compute_centroids(clusters):
    new_centroids = []

    for k in range(len(clusters)):
        r, g, b = 0, 0, 0
        for pixel in clusters[k]:
            r += pixel[0]
            g += pixel[1]
            b += pixel[2]
        r //= len(clusters[k])
        g //= len(clusters[k])
        b //= len(clusters[k])
        new = (r, g, b)
        new_centroids.append(new)

    return new_centroids


# Redraws original image with each pixel replaced with its centroid color.
def draw_replaced_image(im, centroids):
    # load original image and create new image
    pixels = im.load()
    img = Image.new('RGB', (im.width, im.height), "white")
    p = img.load()

    # for each pixel, replace with the color value of the closest centroid
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            RGB_value = centroids[get_min(pixels[x, y], centroids)]
            p[x, y] = RGB_value

    # show and save resulting image
    filename = im.filename.split('/')[-1].split('.')[0]
    img.save(f"{filename}_replaced.jpg")
    img.show()


# Redraws original image with a color palette at the bottom with the centroids.
def draw_palette_image(im, centroids):
    # load original image and create new image
    pixels = im.load()
    addl = im.height // 5  # additional height for color swatch
    img = Image.new('RGB', (im.width, im.height + addl), "white")
    p = img.load()

    # copy over each pixel and add color swatch at the bottom
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            if y >= im.height:
                p[x, y] = centroids[math.floor(x / im.width * len(centroids))]
            else:
                p[x, y] = pixels[x, y]

    # show and save resulting image
    filename = im.filename.split('/')[-1].split('.')[0]
    img.save(f"{filename}_palette.jpg")
    img.show()


# Generate 3D scatter plot of all pixels showing the clusters.
def plot_pixels(filename, clusters, centroids):
    charts = []
    for i in range(len(clusters)):
        charts.append(
            go.Scatter3d(
                name=str(centroids[i]),
                x=[pixel[0] for pixel in clusters[i]],
                y=[pixel[1] for pixel in clusters[i]],
                z=[pixel[2] for pixel in clusters[i]],
                mode='markers',
                marker=dict(
                    size=4,
                    color=f'rgb{str(centroids[i])}',
                ),
                hovertemplate='%{text}',
                text=str(centroids[i])
            )
        )
    fig = go.Figure(charts)
    fig = fig.update_layout(showlegend=False)
    filename = filename.split('/')[-1].split('.')[0]
    fig.write_html(f"{filename}_plot.html")
    fig.show()


# Main processing function.
def main():
    parser = argparse.ArgumentParser(
        description='Generate a color palette from a image using k-means.')
    parser.add_argument("-i", "--img",
                        help='Path to image file.',
                        type=str)
    parser.add_argument("-k", "--k_colors",
                        help='K value i.e. number of colors in palette.',
                        type=int)
    parser.add_argument("-l", "--limit",
                        help='Max number of iterations to test convergence.',
                        type=int, default=20)
    args = parser.parse_args()

    # retrieve filename
    if args.img:
        filename = args.img
    else:
        print("Did not enter filename as command-line argument.")
        filename = input("Enter filename of image: ")

    # retrieve k value
    if args.k_colors:
        k = args.k_colors
    else:
        print("Did not enter k value as command-line argument.")
        k = int(input("Enter K value for number of colors: "))

    cwd = os.path.dirname(os.path.realpath(__file__))
    path = os.path.normpath(os.path.join(cwd, filename))
    if not os.path.isfile(path):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), filename)

    im = Image.open(filename)
    pixels = im.load()

    centroids = []
    old_centroids = []
    i = 0

    # randomizes first choice for centroids from existing pixels
    while len(centroids) < k:
        x = random.randint(0, im.width-1)
        y = random.randint(0, im.height-1)
        cent = pixels[x, y]
        if cent not in centroids:
            centroids.append(cent)

    # continue until converged or until the 20th iteration
    while not converged(centroids, old_centroids) and i < args.limit:
        print(f"Iteration #{i}: {centroids}")
        i += 1
        # find closest centroid for each pixel
        clusters = cluster_pixels(im, centroids)
        # adjust the centroids to the center of the clustered pixels
        centroids = compute_centroids(clusters)

    print("\nConvergence Reached!")
    print(f"Final Centroids: {centroids}")
    colors = ['#%02x%02x%02x' % c for c in centroids]
    print(f"Colors: {colors}")

    # generate image with colors replaced
    draw_replaced_image(im, centroids)
    # generate image with color palette
    draw_palette_image(im, centroids)
    # generate 3D scatter plot of pixels with clustered color
    plot_pixels(im.filename, clusters, centroids)


if __name__ == '__main__':
    main()

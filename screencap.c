//Compile hint: gcc -shared -O3 -lX11 -fPIC -Wl,-soname,prtscn -o prtscn.so prt
#include <X11/X.h>
#include <X11/Xlib.h>

void getScreen(const int, const int, const int, const int, unsigned char *);
void getScreen(const int xx, const int yy, const int w, const int h, unsigned char * output)
{
   Display *display = XOpenDisplay(NULL);
   Window root = DefaultRootWindow(display);

   XImage *image = XGetImage(display,root, xx, yy, w, h, AllPlanes, ZPixmap);

   int x, y;
   int ii = 0;
   for (y = 0; y < h; y++) {
      for (x = 0; x < w; x++) {
         unsigned long pixel = XGetPixel(image, x, y);
         output[ii++] = (pixel & image->red_mask) >> 16;
         output[ii++] = (pixel & image->green_mask) >> 8;
         output[ii++] = (pixel & image->blue_mask);
      }
   }
   XDestroyImage(image);
   XDestroyWindow(display, root);
   XCloseDisplay(display);
}

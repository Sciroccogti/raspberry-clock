#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "GUI_Paint.h"
#include "GUI_BMPfile.h"
#include "ImageData.h"
#include "EPD_2in9.h"
// 2.9inch: 296*128

void  Handler(int signo)
{
    //System Exit
    printf("\r\nHandler:Goto Sleep mode\r\n");
    EPD_Sleep();
    DEV_ModuleExit();

    exit(0);
}

void Paint_MyDrawTime(UWORD Xstart, UWORD Ystart, PAINT_TIME *pTime, sFONT* Font,
                    UWORD Color_Background, UWORD Color_Foreground)
{
    uint8_t value[10] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'};

    UWORD Dx = Font->Width;

    //Write data into the cache
    Paint_DrawChar(Xstart                           , Ystart, value[pTime->Hour / 10], Font, Color_Background, Color_Foreground);
    Paint_DrawChar(Xstart + Dx                      , Ystart, value[pTime->Hour % 10], Font, Color_Background, Color_Foreground);
    if(pTime->Sec % 2)  // if is odd, then clear
    {
        Paint_DrawChar(Xstart + Dx  + Dx / 4 + Dx / 2   , Ystart, ':'                    , Font, Color_Background, Color_Foreground);
    }
    Paint_DrawChar(Xstart + Dx * 2 + Dx / 2         , Ystart, value[pTime->Min / 10] , Font, Color_Background, Color_Foreground);
    Paint_DrawChar(Xstart + Dx * 3 + Dx / 2         , Ystart, value[pTime->Min % 10] , Font, Color_Background, Color_Foreground);
}

int main(int argc, char const *argv[])
{
    printf("Raspberry Clock, launch!\r\n");
    DEV_ModuleInit();

    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    if(EPD_Init(lut_full_update) != 0) {
        printf("e-Paper init failed\r\n");
    }
    EPD_Clear();
    DEV_Delay_ms(500);

    //Create a new image cache
    UBYTE *BlackImage;
    UWORD Imagesize = ((EPD_WIDTH % 8 == 0)? (EPD_WIDTH / 8 ): (EPD_WIDTH / 8 + 1)) * EPD_HEIGHT;
    if((BlackImage = (UBYTE *)malloc(Imagesize)) == NULL) {
        printf("Failed to apply for black memory...\r\n");
        exit(0);
    }
    printf("Paint_NewImage\r\n");
    Paint_NewImage(BlackImage, EPD_WIDTH, EPD_HEIGHT, 270, WHITE);
    Paint_SelectImage(BlackImage);
    Paint_Clear(WHITE);

    // Show time
    printf("show time...\r\n");
    if(EPD_Init(lut_partial_update) != 0) {
        printf("e-Paper init failed\r\n");
    }
    Paint_SelectImage(BlackImage);
    PAINT_TIME sPaint_time;
    char * weekday, * mon;
    struct tm *t;
    time_t tt;
    while(1) {
        time(&tt);
        t = localtime(&tt);        
        sPaint_time.Hour = t->tm_hour;
        sPaint_time.Min = t->tm_min;
        sPaint_time.Sec = t->tm_sec;
        Paint_ClearWindows(0, 48, 0 + Font80.Width * 4.5, 48 + Font80.Height, WHITE);
        Paint_MyDrawTime(0, 48, &sPaint_time, &Font80, WHITE, BLACK);

        switch (t->tm_mon)
        {
            case 0:
                mon = "Jan";
                break;
            case 1:
                mon = "Feb";
                break;
            case 2:
                mon = "Mar";
                break;
            case 3:
                mon = "Apr";
                break;
            case 4:
                mon = "May";
                break;
            case 5:
                mon = "Jun";
                break;
            case 6:
                mon = "Jul";
                break;
            case 7:
                mon = "Aug";
                break;
            case 8:
                mon = "Sep";
                break;
            case 9:
                mon = "Oct";
                break;
            case 10:
                mon = "Nov";
                break;
            case 11:
                mon = "Dec";
                break;
            default:
                break;
        }

        switch (t->tm_wday)
        {
            case 0:
                weekday = "Mon";
                break;
            case 1:
                weekday = "Tue";
                break;
            case 2:
                weekday = "Wed";
                break;
            case 3:
                weekday = "Thur";
                break;
            case 4:
                weekday = "Fri";
                break;
            case 5:
                weekday = "Sat";
                break;
            case 6:
                weekday = "Sun";
                break;
        }

        Paint_ClearWindows(0, 1, 0 + Font46.Width * 9, 1 + Font46.Height, WHITE);
        
        Paint_DrawString_EN(0, 1, weekday, &Font46, WHITE, BLACK);
        Paint_DrawNum(96, 1, t->tm_mday, &Font46, WHITE, BLACK);
        Paint_DrawString_EN(144, 1, mon, &Font46, WHITE, BLACK);

        EPD_Display(BlackImage);
    }

    return 0;
}

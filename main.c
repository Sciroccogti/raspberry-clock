#include <stdlib.h>     //exit()
#include <signal.h>     //signal()
#include <time.h>
#include "GUI_Paint.h"
#include "GUI_BMPfile.h"
#include "ImageData.h"
#include "EPD_2in9.h"
// 2.9inch: 296*128
int main(int argc, char const *argv[])
{
    printf("Raspberry Clock, launch!");
    DEV_ModuleInit();

    // Exception handling:ctrl + c
    signal(SIGINT, Handler);

    if(EPD_Init(lut_full_update) != 0) {
        printf("e-Paper init failed\r\n");
    }
    EPD_Clear();
    DEV_Delay_ms(500);

    // Show time
    printf("show time...\r\n");
    if(EPD_Init(lut_partial_update) != 0) {
        printf("e-Paper init failed\r\n");
    }
    Paint_SelectImage(BlackImage);
    PAINT_TIME sPaint_time;
    struct tm *t;
    time_t tt;
    while(1) {
        time(&tt);
        t = localtime(&tt);        
        sPaint_time.Hour = t->tm_hour;
        sPaint_time.Min = t->tm_min;
        // sPaint_time.Sec = t->tm_sec;
        
        Paint_ClearWindows(0, 48, 0 + Font48.Width * 5, 48 + Font24.Height, WHITE);
        Paint_DrawTime(0, 48, &sPaint_time, &Font48, WHITE, BLACK);
        if(t->tm_sec % 2)  // if is odd, then clear
        {
            Paint_ClearWindows(64, 48, 64 + Font48.Width, 48 + Font24.Height, WHITE);
        }
        EPD_Display(BlackImage);
    }

    return 0;
}

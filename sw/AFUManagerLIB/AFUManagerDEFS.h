//
// Created by lucas on 12/28/17.
//

#ifndef SW_AFU_MANAGER_DEFS_H
#define SW_AFU_MANAGER_DEFS_H

#define AFU_INF_SIZE 64

#define RED          31
#define GREEN        32
#define YELLOW       33
#define BLUE         34

#define MSG(x) cout << "  [APP]  " << x << endl
#define BEGIN_COLOR(c) cout << "\033[1;"<<(c)<<"m";
#define END_COLOR()  cout << "\033[0;m";

#define GET_INDEX(ROW, COL, NUMCOL) (((ROW)*(NUMCOL))+ (COL))
#define MB(x) ((x) << 20) // the same as x*1024*1024
#define GB(x) ((x) << 30) // the same as x*1024*1024*1024

typedef unsigned short afuid_t;
typedef class AFUManager AFUManager_t;

typedef enum CSR_WR {
    REG_CONF_DSM_LOW,
    REG_CONF_DSM_HIGH,
    REG_CONF_IN_LOW,
    REG_CONF_IN_HIGH,
    REG_CONF_OUT_LOW,
    REG_CONF_OUT_HIGH,
    REG_START_AFUs,
    REG_STOP_AFUs,
    REG_RESET_AFUs
} CSR_WR;
typedef enum CSR_RD {
    REG_CLOCK_COUNT,
    REG_CL_WR_COUNT,
    REG_CL_RD_COUNT,
    REG_INF_1,
    REG_INF_2,
    REG_INF_3,
    REG_INF_4,
    REG_INF_5,
    REG_INF_6,
    REG_INF_7,
    REG_INF_8
} CSR_RD;

#endif //SW_AFU_MANAGER_DEFS_H

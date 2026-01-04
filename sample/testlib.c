#include <stdio.h>

#if defined(__GNUC__) || defined(__clang__)
  #define VISIBILITY_DEFAULT __attribute__((visibility("default")))
  #define VISIBILITY_HIDDEN __attribute__((visibility("hidden")))
  #define VISIBILITY_WEAK   __attribute__((weak))
#else
  #define VISIBILITY_DEFAULT
  #define VISIBILITY_HIDDEN
  #define VISIBILITY_WEAK
#endif


/////////////////////////////////////

int func1(int a, int b) {
    return 0;
}

void func2(const char *msg) {
}

/////////////////////////////////////

static int static_func1(int a, int b) {
    return 0;
}

static void static_func2(const char *msg) {
}

/////////////////////////////////////

VISIBILITY_DEFAULT int default_func1(int a, int b) {
    return 0;
}

VISIBILITY_DEFAULT void default_func2(const char *msg) {
}

/////////////////////////////////////

VISIBILITY_HIDDEN int hidden_func1(int a, int b) {
    return 0;
}

VISIBILITY_HIDDEN void hidden_func2(const char *msg) {
}


/////////////////////////////////////

VISIBILITY_WEAK int weak_func1(int a, int b) {
    return 0;
}

VISIBILITY_WEAK void weak_func2(const char *msg) {
}



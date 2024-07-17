#define _BSD_SOURCE
#define _DEFAULT_SOURCE
#define _XOPEN_SOURCE 500
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <limits.h>
#include <sys/utsname.h>
#include <dirent.h>
#include <sys/types.h>
#include <ctype.h>
#include <ifaddrs.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netdb.h>
#include <math.h>
#include <time.h>
#include <errno.h>

#ifdef __linux__
#include <sys/sysinfo.h>
#endif

#include <sys/statvfs.h>
#include <mntent.h>

#define PORT 9111
#define BUFFER_SIZE 4096

typedef unsigned long long disk_size_t;

typedef struct {
    disk_size_t total;
    disk_size_t free;
} DiskSpace;

DiskSpace get_disk_space() {
    FILE* mtab = setmntent("/etc/mtab", "r");
    struct mntent* m;
    struct statvfs s;
    DiskSpace space = {0, 0};

    if (mtab == NULL) {
        perror("setmntent");
        return space;
    }

    while ((m = getmntent(mtab)) != NULL) {
        if (statvfs(m->mnt_dir, &s) == 0) {
            if (strcmp(m->mnt_type, "tmpfs") != 0 && 
                strcmp(m->mnt_type, "devtmpfs") != 0 &&
                strcmp(m->mnt_type, "proc") != 0 &&
                strcmp(m->mnt_type, "sysfs") != 0 &&
                strcmp(m->mnt_type, "devpts") != 0) {
                space.total += (disk_size_t)s.f_blocks * s.f_frsize;
                space.free += (disk_size_t)s.f_bfree * s.f_frsize;
            }
        }
    }

    endmntent(mtab);
    space.total = (space.total + (1ULL << 29)) / (1ULL << 30); // Округляем до ГБ
    space.free = (space.free + (1ULL << 29)) / (1ULL << 30);   // Округляем до ГБ
    return space;
}

double get_uptime() {
    double uptime = 0;
    FILE* f = fopen("/proc/uptime", "r");
    if (f) {
        fscanf(f, "%lf", &uptime);
        fclose(f);
    }
    return uptime;
}

void get_swap_info(unsigned long long* swap_total, unsigned long long* swap_free) {
    FILE* f = fopen("/proc/meminfo", "r");
    if (f) {
        char line[256];
        while (fgets(line, sizeof(line), f)) {
            if (sscanf(line, "SwapTotal: %llu kB", swap_total) == 1) continue;
            if (sscanf(line, "SwapFree: %llu kB", swap_free) == 1) break;
        }
        fclose(f);
        *swap_total /= 1024;
        *swap_free /= 1024;
    }
}

int get_process_count() {
    int count = 0;
    DIR* dir = opendir("/proc");
    if (dir) {
        struct dirent* entry;
        while ((entry = readdir(dir))) {
            if (isdigit(entry->d_name[0])) {
                count++;
            }
        }
        closedir(dir);
    }
    return count;
}

void get_ip_address(char* ip, size_t size) {
    struct ifaddrs *ifaddr, *ifa;
    int family, s;
    char host[NI_MAXHOST];

    if (getifaddrs(&ifaddr) == -1) {
        perror("getifaddrs");
        strncpy(ip, "unknown", size);
        return;
    }

    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr == NULL)
            continue;

        family = ifa->ifa_addr->sa_family;

        if (family == AF_INET) {
            s = getnameinfo(ifa->ifa_addr, sizeof(struct sockaddr_in),
                            host, NI_MAXHOST, NULL, 0, NI_NUMERICHOST);
            if (s != 0) {
                printf("getnameinfo() failed: %s\n", gai_strerror(s));
                continue;
            }

            if (strcmp(ifa->ifa_name, "lo") != 0) {
                strncpy(ip, host, size);
                ip[size - 1] = '\0';
                freeifaddrs(ifaddr);
                return;
            }
        }
    }

    strncpy(ip, "unknown", size);
    freeifaddrs(ifaddr);
}

double get_cpu_usage() {
    static unsigned long long last_total = 0, last_idle = 0;
    unsigned long long user, nice, system, idle, iowait, irq, softirq, steal, total;
    double usage = 0;

    FILE* f = fopen("/proc/stat", "r");
    if (f) {
        if (fscanf(f, "cpu %llu %llu %llu %llu %llu %llu %llu %llu",
                   &user, &nice, &system, &idle, &iowait, &irq, &softirq, &steal) == 8) {
            total = user + nice + system + idle + iowait + irq + softirq + steal;
            if (last_total != 0) {
                unsigned long long total_diff = total - last_total;
                unsigned long long idle_diff = idle - last_idle;
                if (total_diff > 0) {
                    usage = (1.0 - (double)idle_diff / total_diff) * 100.0;
                }
            }
            last_total = total;
            last_idle = idle;
        }
        fclose(f);
    }
    
    usleep(100000);  // 100ms delay
    return usage;
}

char* format_uptime(double uptime) {
    static char buffer[100];
    int days = (int)(uptime / 86400);
    int hours = (int)((uptime / 3600) - (days * 24));
    int minutes = (int)((uptime / 60) - (days * 1440) - (hours * 60));
    snprintf(buffer, sizeof(buffer), "%dd %dh %dm", days, hours, minutes);
    return buffer;
}

double get_load_avg() {
    double loadavg;
    if (getloadavg(&loadavg, 1) == -1) {
        return -1.0;
    }
    return loadavg;
}

char* get_system_info() {
    static char buffer[BUFFER_SIZE];
    char hostname[HOST_NAME_MAX] = "unknown";
    long cpu_cores = 1;
    disk_size_t ram_total = 0, ram_free = 0;
    char kernel[256] = "unknown";
    double uptime = 0;
    unsigned long long swap_total = 0, swap_free = 0;
    int process_count = 0;
    char ip[16] = {0};
    double cpu_usage = 0;

    time_t t = time(NULL);
    struct tm *tm = localtime(&t);
    char datetime[64];
    strftime(datetime, sizeof(datetime), "%Y-%m-%d %H:%M:%S", tm);

#ifdef __linux__
    struct sysinfo si;
    if (sysinfo(&si) == 0) {
        ram_total = (disk_size_t)si.totalram * si.mem_unit / (1024 * 1024);
        ram_free = (disk_size_t)si.freeram * si.mem_unit / (1024 * 1024);
    }
#endif

#ifdef _SC_NPROCESSORS_ONLN
    cpu_cores = sysconf(_SC_NPROCESSORS_ONLN);
#endif

    if (gethostname(hostname, HOST_NAME_MAX) != 0) {
        perror("gethostname");
    }

    DiskSpace disk = get_disk_space();

    struct utsname uts;
    if (uname(&uts) == 0) {
        strncpy(kernel, uts.release, sizeof(kernel) - 1);
        kernel[sizeof(kernel) - 1] = '\0';
    }

    uptime = get_uptime();
    get_swap_info(&swap_total, &swap_free);
    process_count = get_process_count();
    get_ip_address(ip, sizeof(ip));
    cpu_usage = get_cpu_usage();
    double load_avg = get_load_avg();
    char* formatted_uptime = format_uptime(uptime);

    snprintf(buffer, BUFFER_SIZE,
             "DATETIME: %s HOSTNAME: %s CPU: %ld RAM_TOTAL: %llu RAM_FREE: %llu DISK_TOTAL: %llu DISK_FREE: %llu LOAD_AVG: %.2f "
             "KERNEL: %s UPTIME: %s SWAP_TOTAL: %llu SWAP_FREE: %llu PROCESSES: %d IP: %s CPU_USAGE: %.2f%%\n",
             datetime, hostname, cpu_cores, (unsigned long long)ram_total, (unsigned long long)ram_free,
             (unsigned long long)disk.total, (unsigned long long)disk.free, load_avg,
             kernel, formatted_uptime, swap_total, swap_free, process_count, ip, cpu_usage);

    return buffer;
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    int addrlen = sizeof(address);

    // Создаем сокет
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    // Настраиваем опции сокета
  if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt))) {
    perror("setsockopt");
    exit(EXIT_FAILURE);
  }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    // Пытаемся привязать сокет к порту
    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        // Если bind не удался, проверяем, не занят ли порт
        if (errno == EADDRINUSE) {
            fprintf(stderr, "Error: Port %d is already in use\n", PORT);
            exit(21);  // Выход с кодом 21
        } else {
            perror("bind failed");
            exit(EXIT_FAILURE);
        }
    }

    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d\n", PORT);

    while(1) {
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            continue;
        }

        char *info = get_system_info();
        send(new_socket, info, strlen(info), 0);
        close(new_socket);
    }

    return 0;
}

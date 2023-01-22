import numpy as np
import matplotlib.pyplot as plt

labels = ['Baseline', 'PS +30%', 'PS +30%', 'PS \u00B130%', 'PS +50%']
genders = ['Males', 'Females']
male_female_data = np.array([
    [43.4, 43.3],
    [44.8, 44.3],
    [55.6, 53.3],
    [46.2, 45.9],
    [45.3, 44.9]
])


def male_female():
    men_wers = male_female_data.T[0]
    women_wers = male_female_data.T[1]

    ll = len(labels)
    x = np.arange(len(genders))  # the label locations
    width = 0.15  # the width of the bars

    fig, ax = plt.subplots()
    rects = [ax.bar(x - width/2 + (i - (ll // 2)) * width, male_female_data[i], width, label=labels[i]) for i in range(ll)]

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('WER (%)')
    ax.set_title('Error Rates by Gender')
    ax.set_xticks(x, genders)
    ax.legend()

    for i in range(ll):
        ax.bar_label(rects[i], padding=3)

    fig.tight_layout()

    plt.show()
# male_female()


def male_female_2():
    men_wers = male_female_data.T[0]
    women_wers = male_female_data.T[1]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, men_wers, width, label=genders[0])
    rects2 = ax.bar(x + width/2, women_wers, width, label=genders[1])


    ax.set_ylabel('WER (%)')
    ax.set_title('Error Rates by Gender')
    ax.set_xticks(x, labels)
    ax.legend()

    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)

    # plt.show()
    plt.savefig('plots/gender.png')

male_female_2()



labels = ['Baseline', 'PS +30%', 'PS -30%', 'PS \u00B130%', 'PS +50%', 'PS -50%', 'Native Baseline', 'Native \u00B130%']
# compare baseline performances
baseline_data = np.array([43.48, 44.65, 54.41, 46.14, 45.46, 54.19, 60.02, 45.86])

def baseline():
    plt.rcdefaults()
    fig, ax = plt.subplots()


    y_pos = np.arange(len(labels))

    ax.barh(y_pos, baseline_data, align='center')
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('WER (%)')
    ax.set_title('Error Rates for All Combined Speaker Groups')

    # plt.show()
    plt.savefig('plots/combined.png')
baseline()


labels = ['Baseline', 'PS +30%', 'PS \u00B130%', 'PS +50%', 'Native Baseline', 'Native \u00B130%']
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
# compare performance on native Southern Dutch Speech
native_data = np.array([44.47, 46.38, 48.41, 46.47, 43.47, 48.02])

def native():
    plt.rcdefaults()
    ax = ax1

    y_pos = np.arange(len(labels))

    ax.barh(y_pos, native_data, align='center')
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    # ax.set_xlabel('WER (%)')
    ax.set_title('Error Rates for Natives')

native()


# compare performances on nonnative speakers
nonnative_data = np.array([42.06, 42.61, 43.72, 43.29, 68.91, 43.67])

def nonnative():
    plt.rcdefaults()
    ax = ax2

    y_pos = np.arange(len(labels))

    ax.barh(y_pos, nonnative_data, align='center')
    ax.set_yticks(y_pos)
    ax.invert_yaxis()  # labels read top-to-bottom
    # ax.set_xlabel('WER (%)')
    ax.set_title('Error Rates for Non-natives')
nonnative()


# compare child performances
child_data = np.array([52.24, 53.69, 53.61, 53.35, 55.40, 53.66])

def child():
    plt.rcdefaults()
    ax = ax3


    y_pos = np.arange(len(labels))

    ax.barh(y_pos, child_data, align='center')
    ax.set_yticks(y_pos, labels=labels)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('WER (%)')
    ax.set_title('Error Rates for Children')
child()


# compare elderly performances
elderly_data = np.array([52.24, 53.69, 53.61, 53.35, 55.40, 53.66])

def elderly():
    plt.rcdefaults()
    ax = ax4


    y_pos = np.arange(len(labels))

    ax.barh(y_pos, elderly_data, align='center')
    ax.set_yticks(y_pos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('WER (%)')
    ax.set_title('Error Rates for Elderly')

    # plt.show()
    plt.savefig('plots/native-nonnative-child-elder.png')
elderly()



# if __name__ == '__main__':
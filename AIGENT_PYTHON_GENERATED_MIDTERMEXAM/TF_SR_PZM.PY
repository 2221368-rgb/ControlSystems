import control as ct
import matplotlib.pyplot as plt
import numpy as np

def analyze_system(num, den, title):
    
    sys = ct.TransferFunction(num, den)

    print(f"\n{'='*20}")
    print(f"System: {title}")
    print(f"{'='*20}")
    print("Transfer Function G(s):")
    print(sys)

    poles = ct.poles(sys)
    zeros = ct.zeros(sys)
    print(f"Poles: {poles}")
    print(f"Zeros: {zeros}")

    # Visualization
    fig, (ax_step, ax_pz) = plt.subplots(1, 2, figsize=(14, 6))

    # Step Response
    t, y = ct.step_response(sys)
    ax_step.plot(t, y, lw=2, color='#818cf8')
    ax_step.set_title(f'Step Response - {title}', color='white', pad=20)
    ax_step.set_xlabel('Time (s)')
    ax_step.set_ylabel('Amplitude')
    ax_step.grid(True, linestyle='--', alpha=0.3)

    # Pole-Zero Map
    if len(poles) > 0:
        ax_pz.scatter(np.real(poles), np.imag(poles), marker='x', color='#f87171', s=100, label='Poles')
    if len(zeros) > 0:
        ax_pz.scatter(np.real(zeros), np.imag(zeros), marker='o', edgecolors='#22d3ee', facecolors='none', s=100, label='Zeros')
    
    ax_pz.axhline(0, color='white', lw=0.5, alpha=0.5)
    ax_pz.axvline(0, color='white', lw=0.5, alpha=0.5)
    ax_pz.set_title(f'Pole-Zero Map - {title}', color='white', pad=20)
    ax_pz.legend()
    ax_pz.grid(True, linestyle='--', alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Eq 1: s + 1 / (s^4 + 4s^3 + 7s^2 + 6s + 3)
    analyze_system([1, 1], [1, 4, 7, 6, 3], "Equation 1")

    # Eq 2: 1 / (s^4 + 2s^3 + 3s^2 + 2s)
    analyze_system([1], [1, 2, 3, 2, 0], "Equation 2")

    # Eq 3: (4s^2 + 2s + 6) / (16s^4 + 24s^3 + 52s^2 + 36s)
    analyze_system([4, 2, 6], [16, 24, 52, 36, 0], "Equation 3")

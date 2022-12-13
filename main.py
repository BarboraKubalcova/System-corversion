import math
import cv2

city = {
        "JZ": [49.972168, 19.803508],
        "SZ": [50.127540, 19.803508],
        "JV": [49.972168, 20.224255],
        "SV": [50.127540, 20.224255]
    }

def is_city_valid(city: dict) -> bool:
    if city["JZ"][0] != city["JV"][0] or city["SZ"][0] != city["SV"][0]:
        return False
    if city["JZ"][1] != city["SZ"][1] or city["SV"][1] != city["JV"][1]:
        return False
    return True

def calculate_phi_and_psi(hemisphere: str, point: list) -> tuple:
    psi = 90 - point[0] if hemisphere == 'N' else point[0] + 90
    phi = point[1]
    return (phi, psi)

def calculate_cartesian(ro: int, phi: float, psi: float) -> tuple:
    x = ro * math.cos(math.radians(phi)) * math.sin(math.radians(psi))
    y = ro * math.sin(math.radians(phi)) * math.cos(math.radians(psi))
    z = ro * math.cos(math.radians(psi))
    return (x, y, z)

#https://www.theamplituhedron.com/articles/How-to-replicate-the-Arduino-map-function-in-Python-for-Raspberry-Pi/
def _map(x, in_min, in_max, out_min, out_max): 
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#https://www.geeksforgeeks.org/displaying-the-coordinates-of-the-points-clicked-on-the-image-using-python-opencv/
def click_event(event, x, y, flags, params):
    img = cv2.imread('Krakow.jpg', 1)
    height, width, _ = img.shape
    y_spherical = _map(x, 0, width, city["JZ"][1], city["JV"][1])
    x_spherical = _map(y, height, 0, city["JZ"][0], city["SZ"][0])
    phi, psi = calculate_phi_and_psi('N', [x_spherical, y_spherical])
    x_cartesian, y_cartesian, z_cartesian = calculate_cartesian(6378, phi, psi)

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Spherical coordinates: {x_spherical} {y_spherical}")
        print(f"Cartesian coordinates: {x_cartesian} {y_cartesian} {z_cartesian}")
        print(f"Digital coordinates: {x} {y}\n")
        
        # displaying the coordinates
        # on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(img, str(x) + ',' + str(y), (x,y), font, 1, (255, 0, 0), 2)
        cv2.circle(img, (x,y), radius=0, color=(0, 0, 255), thickness=5)
        cv2.imshow('image', img)
 


def main():
    
    if not is_city_valid(city):
        print("City is not in correct format")
        return

    for point in city:
        phi, psi = calculate_phi_and_psi('N', city[point])
        x, y, z = calculate_cartesian(6378, phi, psi)
        print(f"{point} {x} {y} {z}")
    
    img = cv2.imread('Krakow.jpg', 1)
    cv2.imshow('image', img)
    cv2.setMouseCallback('image', click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
        


if __name__ == "__main__":
    main()
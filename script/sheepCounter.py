#!/usr/bin/env python3.12

import cv2
import torch
import numpy as np
import argparse
import sys
import json
import time
from datetime import datetime

class Counter:
    def __init__(self, model_name='yolov5'):
        self.load_model(model_name)
        self.model_name = model_name

    def load_model(self, model_name):
        if model_name == 'yolov5':
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        else:
            raise ValueError('Invalid model name. Please choose from "yolov5".')

    def process_image(self, input_image_path, output_image_path, object_name):
        start_time = time.time()  # Start timing

        img = cv2.imread(input_image_path)
        if img is None:
            raise ValueError(f"Error: Unable to load image from path '{input_image_path}'.")

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.model(img_rgb)
        results.print()

        detections = results.xyxy[0].cpu().numpy()
        total_objects = len(detections)

        for *box, conf, cls in detections:
            xmin, ymin, xmax, ymax = map(int, box)
            confidence = conf
            class_id = int(cls)
            label = self.model.names[class_id]
            if label == object_name:
                cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(img, f'{label} {confidence:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        text = f'Total objects: {total_objects}'
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)[0]
        text_x = img.shape[1] - text_size[0] - 10
        text_y = img.shape[0] - 10
        cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        print(f"Image saved to '{output_image_path}'.")

        cv2.imwrite(f"{output_image_path}output.jpg", img) # output_image_path
        # print(f"Image saved to '{output_image_path}'.")

        end_time = time.time()  # End timing
        process_time = round(end_time - start_time, 2)

        result = {
            "object": object_name,
            "total": total_objects,
            "model": self.model_name,
            "time": datetime.now().isoformat(),
            "process_time": process_time
        }
        with open(f'{output_image_path}verbose.json', 'w') as f:
            json.dump(result, f, indent=4)
        
        

        return json.dumps(result, indent=4)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Input image path', required=True)
    parser.add_argument('-o', '--output', help='Output image path', required=True)
    parser.add_argument('-obj', '--object', help='Object name to detect', required=True)
    parser.add_argument('-m', '--model', help='Model name', required=False, default='yolov5')
    args = parser.parse_args()

    counter = Counter(model_name=args.model)
    result = counter.process_image(args.input, args.output, args.object)
    print(result)

if __name__ == "__main__":
    main()

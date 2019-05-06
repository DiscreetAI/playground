//
//  RoundCorners.swift
//  DataShark
//
//  Created by Gokul Swamy on 12/24/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit

extension UIView {
    func roundedCorners(top: Bool){
        let corners:UIRectCorner = (top ? [.topLeft , .topRight] : [.bottomRight , .bottomLeft])
        let maskPAth1 = UIBezierPath(roundedRect: self.bounds,
                                     byRoundingCorners: corners,
                                     cornerRadii:CGSize(width:40.0, height:40.0))
        let maskLayer1 = CAShapeLayer()
        maskLayer1.frame = self.bounds
        maskLayer1.path = maskPAth1.cgPath
        self.layer.mask = maskLayer1
    }
    
}

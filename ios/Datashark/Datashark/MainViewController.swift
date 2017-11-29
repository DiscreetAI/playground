//
//  MainViewController.swift
//  Datashark
//
//  Created by Gokul Swamy on 11/12/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit
import OAuthSwift
import CoreData

class MainViewController: UIViewController {

    @IBOutlet weak var topStackView: UIStackView!
    @IBOutlet weak var bottomStackRow1View: UIStackView!
    @IBOutlet weak var bottomStackRow2View: UIStackView!
    @IBOutlet weak var walletButton: UIButton!
    
    
    let allNames = ["Facebook", "Fitbit", "Instagram"]
    let name2url = ["Facebook": "URL", "Fitbit": "https://www.fitbit.com/oauth2/authorize", "Instagram": "URL"]
    let name2consumerKey = ["Fitbit": "228MWM"]
    let name2consumerSecret = ["Fitbit": "699ed916a01faff2cb3139f437b897f1"]
    let name2icon = ["Facebook": #imageLiteral(resourceName: "logo_facebook"), "Fitbit": #imageLiteral(resourceName: "logo_fitbit"), "Instagram": #imageLiteral(resourceName: "logo_instagram")]
    let name2scope = ["Fitbit": "sleep"]
    
    var enabledNames: [String] = ["Facebook", "Instagram"]
    var disabledNames: [String] = ["Fitbit"]
    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        let appDelegate = UIApplication.shared.delegate as! AppDelegate
        let context = appDelegate.persistentContainer.viewContext
        let request = NSFetchRequest<NSFetchRequestResult>(entityName: "Service")
        request.returnsObjectsAsFaults = false
        do {
            let result = try context.fetch(request)
            for data in result as! [NSManagedObject] {
                enabledNames.append(data.value(forKey: "name") as! String)
            }
        } catch {
            print("ERROR")
        }
        for name in allNames {
            if !enabledNames.contains(name) {
                disabledNames.append(name)
            }
        }
        
        
        walletButton.layer.cornerRadius = 10
        topStackView.addArrangedSubview(UIView(frame: CGRect(x: 0, y: 0, width: 10, height: 10)))
        var idx = 0
        var enabledIcons: [UIImage] = []
        for name in enabledNames {
            enabledIcons.append(name2icon[name]!)
        }
        for icon in enabledIcons{
            let iconView = UIImageView(image: icon)
            iconView.translatesAutoresizingMaskIntoConstraints = false
            iconView.addConstraint(NSLayoutConstraint(item: iconView,
                                                            attribute: NSLayoutAttribute.height,
                                                            relatedBy: NSLayoutRelation.equal,
                                                            toItem: iconView,
                                                            attribute: NSLayoutAttribute.width,
                                                            multiplier: 1,
                                                            constant: 0))
            iconView.clipsToBounds = true
            iconView.layer.cornerRadius = 22 // T-Swift
            iconView.isUserInteractionEnabled = true
            let tapRecognizer = UITapGestureRecognizer(target: self, action: #selector(enabledAppIconTapped))
            iconView.addGestureRecognizer(tapRecognizer)
            iconView.tag = idx
            topStackView.addArrangedSubview(iconView)
            idx = idx + 1
        }
        
        bottomStackRow1View.addArrangedSubview(UIView(frame: CGRect(x: 0, y: 0, width: 10, height: 10)))
        bottomStackRow2View.addArrangedSubview(UIView(frame: CGRect(x: 0, y: 0, width: 10, height: 10)))
        var disabledIcons: [UIImage] = []
        for name in disabledNames {
            disabledIcons.append(name2icon[name]!)
        }
        var index = 0
        for icon in disabledIcons {
            let iconView = UIImageView(image: convertImageToBW(image: icon))
            iconView.translatesAutoresizingMaskIntoConstraints = false
            iconView.addConstraint(NSLayoutConstraint(item: iconView,
                                                      attribute: NSLayoutAttribute.height,
                                                      relatedBy: NSLayoutRelation.equal,
                                                      toItem: iconView,
                                                      attribute: NSLayoutAttribute.width,
                                                      multiplier: 1,
                                                      constant: 0))
         
            iconView.clipsToBounds = true
            iconView.layer.cornerRadius = 15 // T-Swift
            iconView.alpha = 0.7
            iconView.isUserInteractionEnabled = true
            let tapRecognizer = UITapGestureRecognizer(target: self, action: #selector(disabledAppIconTapped))
            iconView.addGestureRecognizer(tapRecognizer)
            iconView.tag = index
            if index % 2 == 0 {
                bottomStackRow1View.addArrangedSubview(iconView)
            } else {
                bottomStackRow2View.addArrangedSubview(iconView)
            }
            index = index + 1
        }


        // Do any additional setup after loading the view.
    }
    func convertImageToBW(image:UIImage) -> UIImage {
        let filter = CIFilter(name: "CIPhotoEffectMono")
        let ciInput = CIImage(image: image)
        filter?.setValue(ciInput, forKey: "inputImage")
        let ciOutput = filter?.outputImage
        let ciContext = CIContext()
        let cgImage = ciContext.createCGImage(ciOutput!, from: (ciOutput?.extent)!)
        return UIImage(cgImage: cgImage!)
    }
    
    @objc func enabledAppIconTapped(recognizer: UITapGestureRecognizer) {
        let serviceName = disabledNames[recognizer.view!.tag]
        print(serviceName)
    }
    
    @objc func disabledAppIconTapped(recognizer: UITapGestureRecognizer) {
        let serviceName = disabledNames[recognizer.view!.tag]
        let url = name2url[serviceName]
        let consumerKey = name2consumerKey[serviceName]
        let consumerSecret = name2consumerSecret[serviceName]
        let oauthswift = OAuth2Swift(
            consumerKey:    consumerKey!,
            consumerSecret: consumerSecret!,
            authorizeUrl:   url!,
            responseType:   "token"
        )
        let handle = oauthswift.authorize(
            withCallbackURL: URL(string: "oauth-swift://oauth-callback/" + serviceName)!,
            scope: name2scope[serviceName]!,
            state: serviceName,
            success: { credential, response, parameters in
                let token = credential.oauthToken
                let body = ["token": token]
                do{
                    let json = try (JSONSerialization.data(withJSONObject: body, options: JSONSerialization.WritingOptions.prettyPrinted))
                    var request = URLRequest(url: URL(string:"http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/insert/" + serviceName)!)
                    //App Transport Security blocks http:// connections, disable if needed
                    request.httpMethod = "POST" //"GET", ...
                    request.httpBody = json
                    URLSession.shared.dataTask(with: request) { data, response, error in
                        if error != nil {
                            //Your HTTP request failed.
                            print(error?.localizedDescription)
                        } else {
                            //Your HTTP request succeeded
                            print(String(data: data!, encoding: String.Encoding.utf8))
                        }
                        }.resume()
                }
                catch {
                    print("incompatable body")
                }
                let appDelegate = UIApplication.shared.delegate as! AppDelegate
                let context = appDelegate.persistentContainer.viewContext
                let entity = NSEntityDescription.entity(forEntityName: "Service", in: context)
                let newService = NSManagedObject(entity: entity!, insertInto: context)
                newService.setValue(serviceName, forKey: "name")
                do {
                    try context.save()
                } catch {
                    print("Failed saving")
                }
        },
            failure: { error in
                print(error.localizedDescription)
        }
        )
    }


    @IBAction func walletButtonTapped(_ sender: Any) {
        print("button tapped")
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

}

//
//  MainViewController.swift
//  DataShark
//
//  Created by Gokul Swamy on 12/24/17.
//  Copyright © 2017 Gokul Swamy. All rights reserved.
//

import UIKit
import Charts


class ServiceTableViewCell: UITableViewCell {
    @IBOutlet weak var serviceIcon: UIImageView!
    @IBOutlet weak var serviceName: UILabel!
    @IBOutlet weak var serviceProfit: UILabel!
}

class MainViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    var userID: String = ""
    var address: String = ""
    var serviceNames: [String] = []
    var serviceProfits: [Double] = []
    var scopes: [String: [String]] = [:]
    let nameToLogo: [String: UIImage] = ["fitbit": #imageLiteral(resourceName: "Fitbit"), "uber": #imageLiteral(resourceName: "Uber"), "lyft": #imageLiteral(resourceName: "Lyft")] // Needs to be updated with each new service
    
    @IBOutlet weak var chartView: UIView!
    @IBOutlet weak var noDataLabel: UILabel!
    @IBOutlet weak var tableView: UITableView!
    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.delegate = self
        tableView.dataSource = self
        tableView.backgroundColor = .clear
        refreshData()
    }
    
    override func viewDidAppear(_ animated: Bool) {
        refreshData()
    }
    
    func refreshData() {
        var request = URLRequest(url: URL(string:"http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/transactionHistory")!)
        request.httpMethod = "GET"
        request.addValue(address, forHTTPHeaderField: "address")
        URLSession.shared.dataTask(with: request) { data, response, error in
            if error == nil {
                if let data = data {
                    do {
                        let serialized = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                        if let response = serialized{
                            self.serviceNames = Array(response.keys).sorted()
                            self.serviceProfits = []
                            for name in self.serviceNames {
                                let val = Double(String(describing: response[name]!))
                                self.serviceProfits.append(val!)
                            }
                        }
                    } catch {
                        
                    }
                }
            }
            self.createChart(labels: self.serviceNames, values: self.serviceProfits)
            DispatchQueue.main.async { // Required for threading issues
                self.tableView.reloadData()
            }
            }.resume()
    }
    
    func createChart(labels: [String], values: [Double]) {
        DispatchQueue.main.async { // Required for threading issues
            self.chartView.isHidden = true // Just there for shape and error handling
            self.noDataLabel.isHidden = true
            
            let pieChart = PieChartView(frame: self.chartView.frame)
            pieChart.noDataText = "No Data Available."
            
            let total = values.reduce(0, +)
            var str = ""
            if total < 10.0 {
                str = " Total: \n $\(values.reduce(0, +))" // Approximate text centering
            } else {
                str = "  Total: \n $\(values.reduce(0, +))" // Approximate text centering
            }
            
            pieChart.centerAttributedText = NSAttributedString(string: str,
                                                               attributes: [NSAttributedStringKey.foregroundColor: UIColor.white, NSAttributedStringKey.font: UIFont(name: "Nunito-Regular", size: 25.0)!])
            pieChart.holeRadiusPercent = 0.6
            pieChart.holeColor = UIColor.clear
            pieChart.chartDescription = nil
            pieChart.legend.enabled = false
            
            var dataEntries: [ChartDataEntry] = []
            for (index, value) in values.enumerated() {
                let dataEntry = PieChartDataEntry(value: value, label: labels[index])
                dataEntries.append(dataEntry)
            }
            
            let dataset = PieChartDataSet(values: dataEntries, label: nil)
            let red = UIColor(red: 255.0 / 255.0, green: 59.0 / 255.0, blue: 48.0 / 255.0, alpha: 1.0)
            let orange = UIColor(red: 255.0 / 255.0, green: 149.0 / 255.0, blue: 0.0 / 255.0, alpha: 1.0)
            let yellow = UIColor(red: 255.0 / 255.0, green: 204.0 / 255.0, blue: 0.0 / 255.0, alpha: 1.0)
            let purple = UIColor(red: 88.0 / 255.0, green: 86.0 / 255.0, blue: 214.0 / 255.0, alpha: 1.0)
            let pink = UIColor(red: 255.0 / 255.0, green: 45.0 / 255.0, blue: 85.0 / 255.0, alpha: 1.0)
            dataset.colors = [red, orange, yellow, purple, pink]
            
            let data = PieChartData(dataSet: dataset)
            pieChart.data = data
            pieChart.highlightPerTapEnabled = false
            self.view.addSubview(pieChart)
        }
    }
    

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        tableView.deselectRow(at: indexPath, animated: true)
        var request = URLRequest(url: URL(string:"http://datashark7.jn6tkty4uh.us-west-1.elasticbeanstalk.com/userServices")!)
        request.httpMethod = "GET"
        request.addValue(address, forHTTPHeaderField: "address") // Check this for auth
        URLSession.shared.dataTask(with: request) { data, response, error in
            if error == nil {
                if let data = data {
                    do {
                        let serialized = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                        if let response = serialized {
                            self.scopes[self.serviceNames[indexPath.row]] =  (response[self.serviceNames[indexPath.row]] as! String).components(separatedBy: ", ")
                        }
                        self.performSegue(withIdentifier: "mainToService", sender: indexPath)
                    } catch {
                        
                    }
                }
            }
        }.resume()
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "serviceCell", for: indexPath) as! ServiceTableViewCell
        cell.serviceName.text = serviceNames[indexPath.row]
        cell.serviceProfit.text = "$" + String(serviceProfits[indexPath.row])
        
        if (nameToLogo.keys.contains(serviceNames[indexPath.row].lowercased())) {
            cell.serviceIcon.image = self.nameToLogo[serviceNames[indexPath.row].lowercased()]
        } else {
            cell.serviceIcon.image = #imageLiteral(resourceName: "Unknown") // Unknown service
        }
        
        cell.serviceIcon.translatesAutoresizingMaskIntoConstraints = false
        cell.serviceIcon.addConstraint(NSLayoutConstraint(item: cell.serviceIcon,
                                                  attribute: NSLayoutAttribute.height,
                                                  relatedBy: NSLayoutRelation.equal,
                                                  toItem: cell.serviceIcon,
                                                  attribute: NSLayoutAttribute.width,
                                                  multiplier: 1,
                                                  constant: 0))
        cell.serviceIcon.clipsToBounds = true
        cell.serviceIcon.layer.cornerRadius = 22
        
        let bgColorView = UIView()
        bgColorView.backgroundColor = #colorLiteral(red: 0.1098039216, green: 0.7568627451, blue: 0.7568627451, alpha: 1)
        cell.selectedBackgroundView = bgColorView
        
        return cell
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return serviceNames.count
    }
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, heightForRowAt indexPath: IndexPath) -> CGFloat{
        return 100.0
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        if segue.identifier == "mainToSearch" {
            if let destinationVC = segue.destination as? SearchViewController{
                destinationVC.address = self.address
                destinationVC.userID = self.userID
                destinationVC.activeServiceNames = self.serviceNames
            }
        }
        if segue.identifier == "mainToService" {
            if let destinationVC = segue.destination as? ServiceViewController{
                if let idx = sender as? IndexPath {
                    destinationVC.address = self.address
                    destinationVC.userID = self.userID
                    destinationVC.serviceName = self.serviceNames[idx.row]
                    destinationVC.serviceProfit = self.serviceProfits[idx.row]
                    destinationVC.scopes = self.scopes[self.serviceNames[idx.row]]!
                }
            }
        }
        
    }
    
    @IBAction func sendToBank(_ sender: Any) {
        //TODO: Send To Bank
        let alertController = UIAlertController(title: "To Be Implemented", message: "Will be implemented in a future version.", preferredStyle: .alert)
        alertController.addAction(UIAlertAction(title: "OK", style: UIAlertActionStyle.default, handler: nil))
        self.present(alertController, animated: true, completion: nil)
    }

}

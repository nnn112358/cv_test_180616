// g++ homograpy.cpp -I/usr/include/opencv2 -I/usr/include/opencv -L/usr/local/lib -lopencv_core -lopencv_highgui -lopencv_calib3d -lopencv_imgproc

#include <iostream>
#include <opencv2/opencv.hpp>

#include <fstream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

double stof(std::string str){
    double ret;
    std::stringstream ss;
    ss << str;
    ss >> ret;
    return ret;
}

vector<string> split(string &input, char delimiter)
{
    istringstream stream(input);
    string field;
    vector<string> result;
    while (getline(stream, field, delimiter))
    {
        result.push_back(field);
    }
    return result;
}

int main(){
    double xin[4];
    double yin[4];

    double xout[4];
    double yout[4];


    ifstream ifs("data.csv");
    string line;
    int j=0;
    while (getline(ifs, line)){
        vector<string> strvec = split(line, ',');
	if(j==0){
        for (int i = 0; i < 4; i++)        {
            xin[i] = stof(strvec.at(2 * i));
            yin[i] = stof(strvec.at(2 * i + 1));
            cout <<"in_"<< xin[i] << "," << yin[i] << "\t";
        }}
        if(j==1){
        for (int i = 0; i < 4; i++)        {
            xout[i] = stof(strvec.at(2 * i));
            yout[i] = stof(strvec.at(2 * i + 1));
            cout <<"out_"<< xout[i] << "," << yout[i] << "\t";
        }}
       
        j++;
        printf("\n");
    }
    
    vector<cv::Point2f> match_point1;
    vector<cv::Point2f> match_point2;
    
     for (int i = 0; i < 4; i++)    {
     cv::Point2f pts1;
	pts1.x=xin[i];
    	pts1.y=yin[i];

     cv::Point2f pts2;
	pts2.x=xout[i];
    	pts2.y=yout[i];
    	
    	     cout<<pts1<<endl;
             cout<<pts2<<endl;
        match_point1.push_back(pts1);
        match_point2.push_back(pts2);

    }   
    
//    cv::Point2f pts1[] = {cv::Point2f(xin[0], yin[0]), cv::Point2f(xin[1], yin[1]), cv::Point2f(xin[2], yin[2]), cv::Point2f(xin[3], yin[3])};
//    cv::Point2f pts2[] = {cv::Point2f(xout[0], yout[0]), cv::Point2f(xout[1], yout[1]), cv::Point2f(xout[2], yout[2]), cv::Point2f(xout[3], yout[3])};


/*    std::vector<cv::Point2f> obj, scene;
    for (int i = 0; i < 4; i++)    {
        obj.push_back(pts1[i]);
        scene.push_back(pts2[i]);
    }
    */

    cv::Mat H = cv::findHomography(match_point1, match_point2, 0);
    cout << H << endl;
    cout << H.at<double>(0, 0)<<"_"<<H.at<double>(0, 1)<<"_"<<H.at<double>(0, 2) << endl;
    cout << H.at<double>(1, 0)<<"_"<<H.at<double>(1, 1)<<"_"<<H.at<double>(1, 2) << endl;
    cout << H.at<double>(2, 0)<<"_"<<H.at<double>(2, 1)<<"_"<<H.at<double>(2, 2) << endl;

    cv::Mat H2 = cv::getPerspectiveTransform(match_point1, match_point2);
    cout << H2 << endl;
    
    vector<double> x_test;
    vector<double> y_test;
  
    
    ifstream ifs2("input.csv");

    while (getline(ifs2, line)){
        vector<string> strvec = split(line, ',');
          x_test.push_back(stof(strvec.at(0)));
          y_test.push_back(stof(strvec.at(1)));
    }

	for(int i=0;i<x_test.size();i++){
	 cout << x_test[i] << "," << y_test[i] << "\t";
	 
	 
 double x_out=(H.at<double>(0, 0)*x_test[i]+H.at<double>(0, 1)*y_test[i]+H.at<double>(0, 2))/(H.at<double>(2, 0)*x_test[i]+H.at<double>(2, 1)*y_test[i]+H.at<double>(2, 2));
 double y_out=(H.at<double>(1, 0)*x_test[i]+H.at<double>(1, 1)*y_test[i]+H.at<double>(1, 2))/(H.at<double>(2, 0)*x_test[i]+H.at<double>(2, 1)*y_test[i]+H.at<double>(2, 2));
	 
	 	 cout << x_out<< "," << y_out << "\t";
	 
	 printf("\n");
	}







}

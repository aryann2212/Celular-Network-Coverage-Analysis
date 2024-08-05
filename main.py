import json
import random
import sys




def calculate(data):
     

     base_stations=len(data['baseStations'])
     print(f"The total number of base stations ={base_stations}")
     #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     tot_antennas=0
     for bSt in data['baseStations']:
        tot_antennas=tot_antennas+len(bSt['ants'])
     print(f"The total number of antennas ={tot_antennas}")
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     counter=[]
     max_ant=0
     min_ant=0
     avg_ant=0
     for bSt in data['baseStations']:
        tmp=len(bSt['ants'])
        counter.append(tmp)

     max_ant=max(counter)
     min_ant=min(counter)
     avg_ant=sum(counter)/len(counter)

     print(f"The max, min and average of antennas per BS = {max_ant}, {min_ant}, {avg_ant}")

    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     count_pts={}
     tot=0
     for bSt in data['baseStations']:
         for antn in bSt['ants']:
             for pt in antn['pts']:
                 count_pts.setdefault((pt[0],pt[1]),[]).append(pt[2])

     tot=len(count_pts)
     covered_once=0
     for signal in count_pts.values():
         if len(signal)==1:
             covered_once+=1

     
     print(f"The total number of points covered by exactly one antenna = {covered_once}")
     #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

     rep_pts=0
     for t in count_pts.values():
         if len(t)>1:
             rep_pts+=1
             
     print(f"The total number of points covered by more than one antenna = {rep_pts}")
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

     not_covered = (
        (int((data['max_lat'] - data['min_lat']) / data['step']) + 1) *
        (int((data['max_lon'] - data['min_lon']) / data['step']) + 1)
    ) - tot
     
     print(f"The total number of points not covered by any antenna = {not_covered}")
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 
    
     points_cover = {}
     for station in data['baseStations']:
          for antenna in station['ants']:
              for point in antenna['pts']:
                  point_key = (point[0], point[1]) 
                  if point_key in points_cover:
                     points_cover[point_key] += 1
                  else:
                     points_cover[point_key] = 1

     max_coverage = max(points_cover.values())

     print(f"Maximum number of antennas covering one point: {max_coverage}")
    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     points_covered = {}
     for station in data['baseStations']:
         for antenna in station['ants']:
             for point in antenna['pts']:
                 point_key = (point[0], point[1])  
                 points_covered.setdefault(point_key, 0)
                 points_covered[point_key] += 1

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     total_coverages = sum(points_covered.values())
     total_unique_points = len(points_covered)
     if total_unique_points>0:
            average_coverage=total_coverages/total_unique_points

     else:
            average_coverage=0
     

     print(f"Average number of antennas covering a point: {average_coverage:.1f}")
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     tot_possib= (
        (int((data['max_lat'] - data['min_lat']) / data['step']) + 1) *
        (int((data['max_lon'] - data['min_lon']) / data['step']) + 1)
     )

     tot_points=0
     for p in count_pts.values():
           tot_points+=1
     coverage_percentage = (tot_points / tot_possib) * 100
     print(f"The percentage of the covered area = {coverage_percentage:.2f}")
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
     for station in data['baseStations']:
          for antenna in station['ants']:
              u_pts=set((pt[0],pt[1])for pt in antenna['pts'])
              num=len(u_pts)

              if num>max_coverage:
                  max_coverage=num
                  stat_id=station['id']
                  ant_id=antenna['id']

     print(f"The id of the base station and antenna covering the maximum number of points = base station {stat_id}, antenna {ant_id}")
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #*********************************************************************************************************************************************************************************************************
def calc_bSt(data,id=None):
          if id is None:
             base_station = random.choice(data['baseStations'])

          else:
                nid=int(id)-1
                base_station=data['baseStations'][nid]   
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
          total_antennas = len(base_station['ants'])
          print(f"Total number of antennas: {total_antennas}")
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          points_coverage = {}
    
          for antenna in base_station['ants']:
               for point in antenna['pts']:
                   point_key = (point[0], point[1])
                   if point_key not in points_coverage:
                     points_coverage[point_key] = [antenna['id']]
                   else:
                         if antenna['id'] not in points_coverage[point_key]:
                            points_coverage[point_key].append(antenna['id'])

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          covered_once = sum(1 for coverage in points_coverage.values() if len(coverage) == 1)
          print(f"Total number of points covered by exactly one antenna: {covered_once}")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          covered_more_than_once = sum(1 for coverage in points_coverage.values() if len(coverage) > 1)
          print(f"Total number of points covered by more than one antenna: {covered_more_than_once}")
          

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          total_possible_points = ((data['max_lat'] - data['min_lat']) / data['step'] + 1) * ((data['max_lon'] - data['min_lon']) / data['step'] + 1)
    
    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          total_not_covered = total_possible_points - len(points_coverage)
          print(f"Total number of points not covered by any antenna: {total_not_covered}")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          max_antennas_one_point = max(len(coverage) for coverage in points_coverage.values())
          print(f"Maximum number of antennas that cover one point: {max_antennas_one_point}")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          if points_coverage:
             average_number_of_antennas = sum(len(coverage) for coverage in points_coverage.values()) / len(points_coverage)
          else:
             average_number_of_antennas = 0
             print(f"Average number of antennas covering a point: {average_number_of_antennas:.2f}")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          if total_possible_points > 0:
             covered_area_percentage = (len(points_coverage) / total_possible_points) * 100
          else:
           covered_area_percentage = 0
           print(f"Percentage of the covered area by the base station: {covered_area_percentage:.2f}%")

    #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
          antenna_coverage = {}
          for antenna in base_station['ants']:
               covered_points = set((pt[0], pt[1]) for pt in antenna['pts'])
               antenna_coverage[antenna['id']] = len(covered_points)

          max_coverage_antenna_id = max(antenna_coverage, key=antenna_coverage.get)
          print(f"The ID of the antenna that covers the maximum number of points: {max_coverage_antenna_id}")
#*****************************************************************************************************************************************************************************************************************
def nearest_antenna(data, lat, lon):
    nearest_distance = float('inf')
    nearest_antenna = None

    for bs in data['baseStations']:
        for ant in bs['ants']:
            for pt in ant['pts']:
                distance = (pt[0] - lat)**2 + (pt[1] - lon)**2
                if distance < nearest_distance:
                    nearest_distance = distance
                    nearest_antenna = f"Base Station {bs['id']} Antenna {ant['id']}"

    print(nearest_antenna)
#********************************************************************************************************************************************************************************************************************



def main():
    if len(sys.argv)<2:
        print("Use command line in the given format")
        sys.exit()
        

    path=sys.argv[1]
    f=open(path,'r')
    data=json.load(f)
    #print(data)


    while True:
            choice = input("\n1. Display Global Statistics\n2. Display Base Station Statistics\n3. Check Coverage\n4. Exit\nEnter choice: ")
            if choice == '1':
                calculate(data)
            elif choice=='2':
                  print("Choose an option:")
                  print("2.1. Display statistics for a random base station")
                  print("2.2. Choose a station by ID")
                  option = input("Enter your choice (2.1 or 2.2): ")
                  if option == '2.1':
                     
                     calc_bSt(data)  
                  elif option == '2.2':
                      id=0
                      id=input("Enter id:")
                      calc_bSt(data,id)
            
            elif choice == '3':
                lat = float(input("Enter latitude: "))
                lon = float(input("Enter longitude: "))
                nearest_antenna(data, lat, lon)
                
            elif choice == '4':
                print("Thank You")
                break
            else:
                print("Invalid choice. Please try again.")
            

if __name__ == "__main__":
    main()


        
    
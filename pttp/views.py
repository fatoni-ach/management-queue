from django.shortcuts import render, redirect
from django.utils import dateformat
from django.http import HttpResponse, QueryDict
from antrian.models import Pasien
from .forms import TestingForms, TempForms
import csv
import pandas as pd
import time
import datetime
from sklearn import datasets
import numpy as np
from sklearn import metrics

N = 1000
RandomState = 42
TestSize = 0.30

# Create your views here.
def index(request):
    context = {
        'title':'Training Data',
        'body_judul':'Training Data Menggunakan Algoritma Random Forest',
    }

    return render(request, "pttp/index.html", context)

def database(request, tipe):
    context = {
        'title':'Training Data',
        'body_judul':'Training Data Menggunakan Algoritma Random Forest',
    }

    if tipe == 'clasifier':
        df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
        df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
        df = df1

        # print(df['waktu_mulai'])
        df['waktu_mulai'] = pd.to_datetime(df['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
        df['umur'] = pd.cut(np.array(df['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
        df['waktu_berakhir'] = pd.to_timedelta( df['waktu_berakhir'])
        df['waktu_berakhir'] = df['waktu_berakhir'].dt.total_seconds().astype('int64')
        durasi, bins = pd.cut(np.array(df['durasi_pengobatan']),
                bins=5, include_lowest=False,labels=[0 , 1, 2, 3, 4] ,
                 retbins=True)
        df['durasi_pengobatan']= durasi.astype('int64')
        # print(df)

        categorical_feature_mask = df.dtypes==object
        categorical_cols = df.columns[categorical_feature_mask].tolist()
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        # print(df.dtypes)
        df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))
        features = df
        # print(features.dtypes)

        labels = np.array(features['durasi_pengobatan'])
        features= features.drop('durasi_pengobatan', axis = 1)
        features= features.drop('waktu_berakhir', axis = 1)
        # print(features.dtypes)
        feature_list = list(features.columns)
        features = np.array(features)

        from sklearn.model_selection import train_test_split
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = TestSize, random_state = RandomState)

        from sklearn.ensemble import RandomForestClassifier
        rfc = RandomForestClassifier(n_estimators=N, random_state=RandomState)
        rfc.fit(train_features, train_labels)
        pred_labels = rfc.predict(test_features)
        akurasi = str((rfc.score(test_features, test_labels)) *100)
        # print(type(accuracy))

        predictions = rfc.predict(test_features)
        errors = abs(predictions - test_labels)
        # print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
        ab_error = str(round(np.mean(errors), 2))

        average_precision   = str(metrics.precision_score(test_labels, pred_labels, average='weighted')*100)
        recall              = str(metrics.recall_score(test_labels, pred_labels, average='weighted')*100)
        context.update({
            'tipe'          : 'Random Forest Classifier',
            'txt_akurasi'   : 'Akurasi Algoritma : ',
            'akurasi'       : akurasi+ '%',
            'txt_ab_error'  : 'Absolute Error : ',
            'ab_error'      : ab_error+' degrees',
            'txt_presisi'   : 'Presisi : '+average_precision+'%',
            'txt_recall'    : 'Recall   : '+recall+'%',
        })
    elif tipe == 'regressor':
        df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
        df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
        df = df1

        # print(df['waktu_mulai'])
        df['waktu_mulai'] = pd.to_datetime(df['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
        df['umur'] = pd.cut(np.array(df['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
        df['waktu_berakhir'] = pd.to_timedelta( df['waktu_berakhir'])
        df['waktu_berakhir'] = df['waktu_berakhir'].dt.total_seconds().astype('int64')
        # print(df)

        categorical_feature_mask = df.dtypes==object
        categorical_cols = df.columns[categorical_feature_mask].tolist()
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        # print(df.dtypes)
        df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))
        features = df
        # print(features.dtypes)

        labels = np.array(features['durasi_pengobatan'])
        features= features.drop('durasi_pengobatan', axis = 1)
        features= features.drop('waktu_berakhir', axis = 1)
        # print(features.dtypes)
        feature_list = list(features.columns)
        features = np.array(features)

        from sklearn.model_selection import train_test_split
        train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = TestSize, random_state = RandomState)

        from sklearn.ensemble import RandomForestRegressor
        # Instantiate model with 1000 decision trees
        rfr = RandomForestRegressor(n_estimators = N, random_state = RandomState)
        # Train the model on training data
        rfr.fit(train_features, train_labels);
        pred_labels = rfr.predict(test_features)

        predictions = rfr.predict(test_features)
        errors = abs(predictions - test_labels)
        # print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
        ab_error = str(round(np.mean(errors), 2))

        mape = 100 * (errors / test_labels)
        accuracy = 100 - np.mean(mape)
        # print('Accuracy:', round(accuracy, 2), '%.')
        akurasi = str(round(accuracy, 2))

        context.update({
            'tipe'          : 'Random Forest Regressor',
            'txt_akurasi'   : 'Akurasi Algoritma : ',
            'akurasi'       : akurasi+'%',
            'txt_ab_error'  : 'Mean Absolute Error : ',
            'ab_error'      : ab_error+' degrees',
        })

    return render(request, "pttp/index.html", context)

def export(request, tipe):
    # response = HttpResponse(content_type='text/csv')
    # response['Content-Disposition']='attachment; filename="users.csv"'
    # writer = csv.writer(response)
    # writer.writerow(['id', 'nama_pasien','jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan'])
    # users = Pasien.objects.all().values_list('id','nama_pasien','jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')
    # for user in users:
    #     writer.writerow(user)
    #     print(user)
    # return response
    # heading = (['id', 'nama_pasien', 'jenis_kelamin'])
    # users = Pasien.objects.all().values_list('id', 'nama_pasien', 'jenis_kelamin')
    # for user in users:
    #     heading.append(user)

    # print(heading)

    # df = pd.DataFrame(list(Pasien.objects.all().values_list('id', 'nama_pasien', 'jenis_kelamin')))
    # print(df)
    
    context = {
        'title':'Training Data',
        'body_judul':'Training Data Menggunakan Algoritma Random Forest',
        'tipe':tipe,
    }

    if request.method == "POST":
        tipe = "database_done"
        context.update({
            'message':'Database berhasil di Training',
            'tipe':'done'
        })
    return render(request, "pttp/index.html", context)

def export_iris(request, tipe):
    context={
        'title':'Training Data',
        'body_judul':'Training Data menggunakan algoritma Random Forest',
        'tipe':tipe,
    }
    if request.method == "POST":
        print(request.POST['tree'])
        tree = int(request.POST['tree'])
        iris = datasets.load_iris()
        data=pd.DataFrame({
            'sepal length':iris.data[:,0],
            'sepal width':iris.data[:,1],
            'petal length':iris.data[:,2],
            'petal width':iris.data[:,3],
            'species':iris.target
        })
        #print(data.head())
        from sklearn.model_selection import train_test_split
        X=data[['sepal length', 'sepal width', 'petal length', 'petal width']]
        # Features
        y=data['species']
        # Labels

        # Split dataset into training set and test set
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TestSize)
        # 70% training and 30% test

        #Import Random Forest Model
        from sklearn.ensemble import RandomForestClassifier

        #Create a Gaussian Classifier
        clf=RandomForestClassifier(n_estimators=N)

        #Train the model using the training sets y_pred=clf.predict(X_test)
        clf.fit(X_train,y_train)

        y_pred=clf.predict(X_test)
        #print(y_pred)
        #Import scikit-learn metrics module for accuracy calculation
        from sklearn import metrics
        # Model Accuracy, how often is the classifier correct?
        #print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

        #print(clf.predict([[3, 5, 4, 2]]))
        tipe="done"
        context.update({
            'message':'Dataset IRIS berhasil di training',
            'tipe':'done'
        })

    return render(request, "pttp/index.html", context)

def convert_time(request):
    context = {
        'title':'Training Data',
        'body_judul':'Training Data menggunakan algoritma Random Forest',
    }
    pasien = Pasien.objects.all()
    for pas in pasien:
        print(pas.waktu_mulai[0:8])
        pas.waktu_mulai=pas.waktu_mulai[0:8]
        pas.waktu_berakhir=pas.waktu_berakhir[0:8]
        pas.save()

    return render(request, "pttp/index.html", context)

def get_duration(request):
    context = {
        'title':'Training Data',
        'body_judul':'Training Data menggunakan algoritma Random Forest',
    }
    pasien = Pasien.objects.all()
    for pas in pasien:
        time1 = datetime.datetime.strptime(pas.waktu_mulai, '%H:%M:%S')
        time2 = datetime.datetime.strptime(pas.waktu_berakhir, '%H:%M:%S')
        durasi = time2-time1
        d = int(durasi.total_seconds())
        pas.durasi_pengobatan = d
        pas.save()

    return render(request, "pttp/index.html", context)


# def testing(request):
#     pasien_form = TempForms(request.POST.copy(), request.FILES or None)
#     context = {
#         'title':'Testing Data',
#         'body_judul':'Testing Data menggunakan algoritma Random Forest',
#         'pasien_form':pasien_form,
#     }
#     if request.method == "POST":
#         csv_file = request.FILES['csv']
#         if pasien_form.is_valid():
#             df1 = pd.read_csv(csv_file)
#             df =df1

#         # df = pd.read_csv(temp)
#             # print(df.dtypes)
#             categorical_feature_mask = df.dtypes==object
#             categorical_cols = df.columns[categorical_feature_mask].tolist()
#             from sklearn.preprocessing import LabelEncoder
#             le = LabelEncoder()
#             df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))
#             features = df

#             labels = np.array(features['friend'])
#             features= features.drop('friend', axis = 1)
#             feature_list = list(features.columns)
#             features = np.array(features)

#             from sklearn.model_selection import train_test_split
#             train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = 0.25, random_state = 42)

#             ############PAKAI RANDOM FOREST CLASSIFIER#######################################################
#             from sklearn.ensemble import RandomForestClassifier
#             rfc = RandomForestClassifier(n_estimators=500, random_state=0)
#             rfc.fit(train_features, train_labels)

#             a={(int(pasien_form.data['year']),
#                 int(pasien_form.data['month']),
#                 int(pasien_form.data['day']),
#                 pasien_form.data['week'],
#                 int(pasien_form.data['temp_2']),
#                 int(pasien_form.data['temp_1']),
#                 float(pasien_form.data['average']),
#                 int(pasien_form.data['actual']),
#                 int(pasien_form.data['forecast_noaa']),
#                 int(pasien_form.data['forecast_acc']),
#                 int(pasien_form.data['forecast_under'])
#                 )} #29
#             a = pd.DataFrame(a)
#             a.columns = ["year","month","day","week","temp_2","temp_1","average","actual","forecast_noaa","forecast_acc","forecast_under"]
#             temp = df1
#             # print(a.dtypes)
#             b = a.append(temp)
#             # print(b.dtypes)
#             categorical_feature_mask = b.dtypes==object
            
#             categorical_cols = b.columns[categorical_feature_mask].tolist()
#             # print(categorical_cols)
#             # b[categorical_cols] = le.fit_transform(b[categorical_cols])
#             # print(b[categorical_cols].dtypes)

#             b[categorical_cols] = b[categorical_cols].apply(lambda col: le.fit_transform(col.astype(str)))
#             b= b.drop('friend', axis = 1)
#             hasil = (rfc.predict(b.head(1)))
#             hasil = int(hasil)

#             print(hasil)
#             context.update({
#                 'hasil':hasil,
#             })

    
#     return render(request, "pttp/testing.html", context)


# def regressor():
#     from sklearn.ensemble import RandomForestRegressor# Instantiate model with 1000 decision trees
#     rf = RandomForestRegressor(n_estimators = 1000, random_state = 42)# Train the model on training data
#     rf.fit(train_features, train_labels);
#     predictions = rf.predict(test_features)
#     errors = abs(predictions - test_labels)
#     print('Mean Absolute Error:', round(np.mean(errors), 2), 'degrees.')
#     mape = 100 * (errors / test_labels)
#     accuracy = 100 - np.mean(mape)
#     print('Accuracy:', round(accuracy, 2), '%.')

def testing(request):
    pasien_form = TestingForms(request.POST.copy() or None)
    # time = datetime.datetime.now().time().isoformat(timespec='seconds')
    # print(time)
    context = {
        'title':'Testing Data',
        'body_judul':'Testing Data Menggunakan Algoritma Random Forest',
        'pasien_form': pasien_form,
    }
    if request.method == "POST":
        # csv_file = request.FILES['csv']
        if request.POST['tipe'] == 'classifier':
            if pasien_form.is_valid():

                df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
                df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
                df = df1

                df['waktu_mulai'] = pd.to_datetime(df['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
                #df['waktu_mulai'] = pd.to_timedelta( df['waktu_mulai'])
                #df['waktu_mulai'] = df['waktu_mulai'].dt.hour.astype('int64')
                df['umur'] = pd.cut(np.array(df['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
                durasi, bins = pd.cut(np.array(df['durasi_pengobatan']),
                                bins=5, include_lowest=False,labels=[0 , 1, 2, 3, 4] ,
                                retbins=True)
                df['durasi_pengobatan']= durasi.astype('int64')
                df['waktu_berakhir'] = pd.to_timedelta( df['waktu_berakhir'])
                df['waktu_berakhir'] = df['waktu_berakhir'].dt.total_seconds().astype('int64')
                # print(df)

                categorical_feature_mask = df.dtypes==object
                categorical_cols = df.columns[categorical_feature_mask].tolist()
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                # print(df.dtypes)
                df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))
                features = df
                # print(features.dtypes)

                labels = np.array(features['durasi_pengobatan'])
                features= features.drop('durasi_pengobatan', axis = 1)
                features= features.drop('waktu_berakhir', axis = 1)
                # print(features.dtypes)
                feature_list = list(features.columns)
                features = np.array(features)

                from sklearn.model_selection import train_test_split
                train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = TestSize, random_state = RandomState)

                from sklearn.ensemble import RandomForestClassifier
                rfc = RandomForestClassifier(n_estimators=N, random_state=RandomState)
                rfc.fit(train_features, train_labels)
                time = datetime.datetime.now().time().isoformat(timespec='seconds')
                a={(pasien_form.data['jenis_kelamin'],
                    int(pasien_form.data['umur']),
                    pasien_form.data['nama_dokter'],
                    pasien_form.data['jenis_pengobatan'],
                    time,
                    '10:15:29',
                    int(0),
                    )} #29
                a = pd.DataFrame(a)
                a.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
                
                df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
                df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
                
                temp = df1
                # print(a['waktu_mulai'])
                b = a.append(temp)
                b['waktu_mulai'] = pd.to_datetime(b['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
                b['umur'] = pd.cut(np.array(b['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
                # print(b.dtypes)
                categorical_feature_mask = b.dtypes==object
                
                categorical_cols = b.columns[categorical_feature_mask].tolist()
                # print(categorical_cols)
                # b[categorical_cols] = le.fit_transform(b[categorical_cols])
                # print(b[categorical_cols].dtypes)

                b[categorical_cols] = b[categorical_cols].apply(lambda col: le.fit_transform(col.astype(str)))
                b= b.drop('durasi_pengobatan', axis = 1)
                b= b.drop('waktu_berakhir', axis = 1)
                # print(b.dtypes)
                hasil_array = rfc.predict(b.head(1))
                # print(bins[hasil+1])
                hasil = int(bins[hasil_array+1])
                menit = int(hasil/60)
                detik = int(hasil%60)
                menit = str(menit)
                detik = str(detik)

                context.update({
                    'prediksi':' Prediksi lamanya Berobat ',
                    'menit': 'Menit',
                    'hasil' : menit+':'+detik,
                    'hasil1' : str(hasil_array+1),
                    'binz'      : str(bins),
                    'txt_prediksi' : 'Output Sebenarnya',
                })
        elif request.POST['tipe'] == 'regressor':
            if pasien_form.is_valid():

                df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
                df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
                df = df1

                # print(df['waktu_mulai'])
                df['waktu_mulai'] = pd.to_datetime(df['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
                #df['waktu_mulai'] = pd.to_timedelta( df['waktu_mulai'])
                #df['waktu_mulai'] = df['waktu_mulai'].dt.hour.astype('int64')
                df['umur'] = pd.cut(np.array(df['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
                df['waktu_berakhir'] = pd.to_timedelta( df['waktu_berakhir'])
                df['waktu_berakhir'] = df['waktu_berakhir'].dt.total_seconds().astype('int64')
                # print(df)

                categorical_feature_mask = df.dtypes==object
                categorical_cols = df.columns[categorical_feature_mask].tolist()
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                # print(df.dtypes)
                df[categorical_cols] = df[categorical_cols].apply(lambda col: le.fit_transform(col))
                features = df
                # print(features.dtypes)

                labels = np.array(features['durasi_pengobatan'])
                features= features.drop('durasi_pengobatan', axis = 1)
                features= features.drop('waktu_berakhir', axis = 1)
                # print(features.dtypes)
                feature_list = list(features.columns)
                features = np.array(features)

                from sklearn.model_selection import train_test_split
                train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size = TestSize, random_state = RandomState)

                # Import the model we are using
                from sklearn.ensemble import RandomForestRegressor
                # Instantiate model with 1000 decision trees
                rfr = RandomForestRegressor(n_estimators = N, random_state = RandomState)
                # Train the model on training data
                rfr.fit(train_features, train_labels);

                time = datetime.datetime.now().time().isoformat(timespec='seconds')
                a={(pasien_form.data['jenis_kelamin'],
                    int(pasien_form.data['umur']),
                    pasien_form.data['nama_dokter'],
                    pasien_form.data['jenis_pengobatan'],
                    time,
                    '10:15:29',
                    int(0),
                    )} #29
                a = pd.DataFrame(a)
                a.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
                
                df1 = pd.DataFrame(list(Pasien.objects.all().values_list('jenis_kelamin', 'umur', 'nama_dokter', 'jenis_pengobatan','waktu_mulai', 'waktu_berakhir', 'durasi_pengobatan')))
                df1.columns = ["jenis_kelamin", "umur", "nama_dokter", "jenis_pengobatan","waktu_mulai", "waktu_berakhir", "durasi_pengobatan"]
                
                temp = df1
                # print(a['waktu_mulai'])
                b = a.append(temp)
                b['waktu_mulai'] = pd.to_datetime(b['waktu_mulai'], format='%H:%M:%S').dt.hour.astype('int64')
                #df['waktu_mulai'] = pd.to_timedelta( df['waktu_mulai'])
                #df['waktu_mulai'] = df['waktu_mulai'].dt.hour.astype('int64')
                b['umur'] = pd.cut(np.array(b['umur']), [0,12,26,45,100],labels=[0, 1, 2, 3], include_lowest=False).astype('int64')
                # print(b.dtypes)
                categorical_feature_mask = b.dtypes==object
                
                categorical_cols = b.columns[categorical_feature_mask].tolist()
                # print(categorical_cols)
                # b[categorical_cols] = le.fit_transform(b[categorical_cols])
                # print(b[categorical_cols].dtypes)

                b[categorical_cols] = b[categorical_cols].apply(lambda col: le.fit_transform(col.astype(str)))
                b= b.drop('durasi_pengobatan', axis = 1)
                b= b.drop('waktu_berakhir', axis = 1)
                # print(b.dtypes)
                hasil = (rfr.predict(b.head(1)))
                menit = int(hasil/60)
                detik = int(hasil%60)
                menit = str(menit)
                detik = str(detik)

                context.update({
                    'prediksi':' Prediksi lamanya Berobat ',
                    'menit': 'Menit',
                    'hasil' : menit+':'+detik,
                    'hasil1' : str(hasil),
                    'txt_prediksi' : 'Output Sebenarnya',
                    'tipe' : request.POST['tipe']
                })
    
    return render(request, 'pttp/testing.html', context)


    # from sklearn.ensemble import RandomForestClassifier
    # clf=RandomForestClassifier(n_estimators=100)
    # clf.fit(X_train,y_train)
    # y_pred=clf.predict(X_test)
    # from sklearn import metrics
    # print("Accuracy:",metrics.accuracy_score(y_test, y_pred)*100," %")
    # print(y_pred)
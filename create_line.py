import pandas as pd


def createline(streetname, filename, df):
    lon = list(dfr[dfr['XZQMC'] == streetname]['Longitude'])[0]
    lat = list(dfr[dfr['XZQMC'] == streetname]['Latitude'])[0]
    writer = open(filename, 'a', encoding='utf-8')
    count = 0
    writer.write('LineID,Order,O,D,Longitude,Latitude\n')
    for row in df.itertuples():
        count += 1
        if getattr(row, 'XZQMC') == streetname:
            count -= 1
            continue
        # print(getattr(row,'XZQMC'),getattr(row,'Longitude'),getattr(row,'Latitude'))
        writer.write(str(count) + ',' + '0' + ',' + getattr(row, 'XZQMC') + ',' + streetname + ',' + str(
            getattr(row, 'Longitude')) + ',' + str(getattr(row, 'Latitude')) + '\n' + str(
            count) + ',' + '1' + ',' + getattr(row, 'XZQMC') + ',' + streetname + ',' + str(lon) + ',' + str(
            lat) + '\n')
    writer.close()


if __name__ == '__main__':
    df = pd.read_excel(r'G:\参考资料与工具\深圳街道中心点坐标.xlsx')
    filename = r'G:\参考资料与工具\line.txt'
    streetname = '石岩街道'
    createline(streetname, filename, df)

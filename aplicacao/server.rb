require 'socket'
require 'uri'

# O arquivos virão da pasta public, dentro da raiz do projeto 
WEB_ROOT = './public'

# Mapa das extensões do tipo de arquivo 
CONTENT_TYPE_MAPPING = {
  'html' => 'text/html',
  'txt' => 'text/plain',
  'png' => 'image/png',
  'jpg' => 'image/jpeg'
}

# Trata os dados binarios se o tipo de conteudo do arquivo nao for encontrado
DEFAULT_CONTENT_TYPE = 'application/octet-stream'


# Essa função faz um parse da extensão do arquivo  
# requisitado e então olha o tipo do conteudo do arquivo

def content_type(path)
  ext = File.extname(path).split(".").last
  CONTENT_TYPE_MAPPING.fetch(ext, DEFAULT_CONTENT_TYPE)
end


# Essa função faz um parse da Request-Line e 
# gera um caminho para o arquivo no servidor

def requested_file(request_line)
  request_uri  = request_line.split(" ")[1]
  path         = URI.unescape(URI(request_uri).path)

  File.join(WEB_ROOT, path)
end

# Set do serivdor 
server = TCPServer.new('127.0.0.1', 2345)

loop do
  socket       = server.accept
  request_line = socket.gets

  STDERR.puts request_line

  path = requested_file(request_line)
  print(path)
  path = File.join(path, 'index.html') if File.directory?(path)
  
  
  # Verifica se o arquivo existe e se nao um diretorio
  # antes de tentar abrir
  if File.exist?(path) && !File.directory?(path)
    File.open(path, "rb") do |file|
      print "HTTP/1.1 200 OK\r\n" +
                   "Content-Type: #{content_type(file)}\r\n" +
                   "Content-Length: #{file.size}\r\n" +
                   "Content-Type: #{content_type(file)}\r\n" +
                   "Content-Length: #{file.size}\r\n" +
                   "Connection: close\r\n"


      socket.print "HTTP/1.1 200 OK\r\n" +
                   "Content-Type: #{content_type(file)}\r\n" +
                   "Content-Length: #{file.size}\r\n" +
                   "Content-Type: #{content_type(file)}\r\n" +
                   "Content-Length: #{file.size}\r\n" +
                   "Connection: close\r\n"

      socket.print "\r\n"

      # escreve o conteudo do arquivo no socket
      IO.copy_stream(file, socket)
  end
  else
     message = "File not found\n"


    # responde com 404 para indicar que arquivo nao existe no curl --verbose
    socket.print "HTTP/1.1 404 Not Found\r\n" +
                 "Content-Type: text/plain\r\n" +
                 "Content-Length: #{message.size}\r\n" +
                 "Connection: close\r\n"

    socket.print "\r\n"

    socket.print message
  end

  socket.close
end
